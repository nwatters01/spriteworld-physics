"""Config for springs system.

This is a system of random shapes that collide and bounce of the walls.

To demo this task, navigate to the main directory and run the following:
'''
$ python demo.py --config=spriteworld_physics.configs.collisions \
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
from spriteworld import sprite_generators
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
        distribs.Discrete('shape', ['circle', 'square', 'triangle']),
        distribs.Discrete('scale', [0.1]),
        distribs.Continuous('c0', 0, 1),
        distribs.Continuous('c1', 0.5, 1.),
        distribs.Discrete('c2', [1.]),
        distribs.Continuous('x_vel', -0.03, 0.03),
        distribs.Continuous('y_vel', -0.03, 0.03),
        distribs.Continuous('mass', 0.5, 2.0),
    ])

    sprite_gen = generate_sprites.generate_sprites(
        factors, num_sprites=lambda: np.random.randint(4, 8))

    # The collisions are simulated by applying an invisible rigid circular shell
    # around each sprite. The shell_radius of 0.08 is eye-balled to look
    # reasonable.
    force = forces.SymmetricShellCollision(shell_radius=0.08)
    graph_generator = graph_generators.LowerTriangular(force=force)

    renderers = {
        'image':
            spriteworld_renderers.PILRenderer(
                image_size=(64, 64), anti_aliasing=5)
    }

    config = {
        'graph_generators': (graph_generator,),
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
