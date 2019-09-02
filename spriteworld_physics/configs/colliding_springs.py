"""Config for colliding springs system.

This is a system of 4 circles which are fully connected by springs and collide.

To demo this task, navigate to the main directory and run the following:
'''
$ python demo.py --config=spriteworld_physics.configs.colliding_springs \
    --hsv_colors=True
'''
"""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os
from spriteworld import factor_distributions as distribs
from spriteworld import renderers as spriteworld_renderers
from spriteworld_physics import forces
from spriteworld_physics import generate_sprites
from spriteworld_physics import graph_generators


def get_config(mode=None):
    """Generate environment config.

    Args:
        mode: Unused task mode.

    Returns:
        config: Dictionary defining task/environment configuration. Can be fed
            as kwargs to physics_environment.PhysicsEnvironment.
    """

    # Factor distributions for the sprites.
    factors = distribs.Product([
        distribs.Continuous('x', 0.1, 0.9),
        distribs.Continuous('y', 0.1, 0.9),
        distribs.Discrete('shape', ['circle']),
        distribs.Discrete('scale', [0.1]),
        distribs.Continuous('c0', 0, 1),
        distribs.Continuous('c1', 0.5, 1.),
        distribs.Discrete('c2', [1.]),
        distribs.Continuous('x_vel', -0.02, 0.02),
        distribs.Continuous('y_vel', -0.02, 0.02),
        distribs.Discrete('mass', [1.]),
    ])

    sprite_gen = generate_sprites.generate_sprites(
        factors, num_sprites=4)

    spring_force = forces.Spring(spring_constant=0.01, spring_equilibrium=0.25)
    spring_graph_generator = graph_generators.FullyConnected(
        force=spring_force)
    collision_force = forces.SymmetricShellCollision(shell_radius=0.08)
    collision_graph_generator = graph_generators.LowerTriangular(
        force=collision_force)

    renderers = {
        'image':
            spriteworld_renderers.PILRenderer(
                image_size=(64, 64), anti_aliasing=5)
    }

    config = {
        'graph_generators': (spring_graph_generator, collision_graph_generator),
        'renderers': renderers,
        'init_sprites': sprite_gen,
        'episode_length': 30,
        'bounce_off_walls': True,
        'physics_steps_per_env_step': 10,
        'metadata': {
            'name': os.path.basename(__file__),
            'mode': mode
        }
    }
    return config
