"""Physics environment in Spriteworld."""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from spriteworld import environment
from spriteworld import tasks
import numpy as np
import six
import dm_env


class PhysicsEnvironment(environment.Environment):
    """Physics environment class in Spriteworld.

    This environment inherits from spriteworld.environment.Environment. For
    details, see https://github.com/deepmind/spriteworld.
    """

    def __init__(self,
                 graph_generators,
                 renderers,
                 init_sprites,
                 bounce_off_walls=True,
                 episode_length=10,
                 physics_steps_per_env_step=1,
                 metadata=None):
        """Construct environment with physics in Spriteworld.

        This environment simulates the forces specified in graph_generators with
        Newton's method. This is very simple yet can yield high compounding
        error of the simulator. To increase the physical accuracy of the
        simulation, increase physics_steps_per_env_step.

        Args:
            graph_generators: Iterable of instances of subclasses of
                graph_generators.AbstracGraphGenerator. Each element is used to
                apply forces between the sprites.
            renderers: Dict where values are renderers and keys are names,
                reflected in the keys of the observation.
            init_sprites: Callable returning iterable of sprites, called upon
                environment reset.
            bounce_off_walls: Bool. Whether to keep sprites in frame by making
                them bounce elastically off the frame edges.
            episode_length: Number of steps per episode.
            physics_steps_per_env_step: Int. Number of steps of physics
                simulation to perform each environment step. If not 1, forces
                are re-normalized to account for this and make the acceleration
                per environment step independ of physics_steps_per_env_step.
            metadata: Optional metadata to be added to the global_state.
        """
        self._graph_generators = graph_generators
        self._renderers = renderers
        self._init_sprites = init_sprites
        self._bounce_off_walls = bounce_off_walls
        self._episode_length = episode_length
        self._physics_steps_per_env_step = physics_steps_per_env_step
        self._metadata = metadata

        self._physics_delta_t = 1. / physics_steps_per_env_step
        self._sprites = self._init_sprites()
        self._step_count = 0
        self._reset_next_step = True
        self._renderers_initialized = False
        self._task = tasks.NoReward()

    def reset(self):
        """Reset the environment and re-generate the interaction graphs."""
        timestep = super(PhysicsEnvironment, self).reset()
        self._graphs = [graph_gen.generate_graph(self._sprites)
                        for graph_gen in self._graph_generators]
        return timestep

    def should_terminate(self):
        return self._step_count >= self._episode_length

    def physics_step(self):
        """Apply forces and update sprite positions/velocities."""
        # Apply forces to sprites
        for graph in self._graphs:
            for i, acting_sprite in enumerate(self._sprites):
                for j, receiving_sprite in enumerate(self._sprites):
                    graph[i][j].apply_force(
                        acting_sprite, receiving_sprite,
                        force_multiplier=self._physics_delta_t)

        # Update sprite positions from their velocities
        for sprite in self._sprites:
            sprite.update_position(bounce_off_walls=self._bounce_off_walls,
                                   delta_t=self._physics_delta_t)

    def step(self):
        """Step the environment, returning an observation."""
        if self._reset_next_step:
            return self.reset()

        self._step_count += 1

        for _ in range(self._physics_steps_per_env_step):
            self.physics_step()

        observation = self.observation()

        if self.should_terminate():
            self._reset_next_step = True
            return dm_env.termination(reward=0, observation=observation)
        else:
            return dm_env.transition(reward=0, observation=observation)

    def action_spec(self):
        return None

    @property
    def action_space(self):
        return None
