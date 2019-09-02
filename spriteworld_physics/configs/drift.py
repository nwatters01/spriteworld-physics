"""Config for drift system.

This is a system of circles that drift with constant velocity, do not interact,
and do not bounce of the walls.

This config has a train mode and a test mode. In the train mode there are 3-5
sprites, yet in the test mode there are 6-11.

To demo this task, navigate to the main directory and run the following:
'''
$ python demo.py --config=spriteworld_physics.configs.drift \
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

_NUM_SPRITES = {
    'train': lambda: np.random.randint(3, 6),
    'test': lambda: np.random.randint(6, 12),
}


def get_config(mode='train'):
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
        distribs.Discrete('c1', [1.]),
        distribs.Discrete('c2', [1.]),
        distribs.Continuous('x_vel', -0.03, 0.03),
        distribs.Continuous('y_vel', -0.03, 0.03),
        distribs.Discrete('mass', [1]),
    ])

    num_sprites = _NUM_SPRITES[mode]
    sprite_gen = generate_sprites.generate_sprites(
        factors, num_sprites=num_sprites)

    graph_generator = graph_generators.FullyConnected(force=forces.NoForce)

    renderers = {
        'image':
            spriteworld_renderers.PILRenderer(
                image_size=(64, 64), anti_aliasing=5)
    }

    config = {
        'graph_generators': (graph_generator,),
        'renderers': renderers,
        'init_sprites': sprite_gen,
        'episode_length': 20,
        'bounce_off_walls': False,
        'metadata': {
            'name': os.path.basename(__file__),
            'mode': mode
        }
    }
    return config
