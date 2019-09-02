"""Config for magnets system.

This is a system of a large yellow immobile circle that exerts gravitational
forces on 4 smaller star-shaped sprites.

This config exemplifies the use of graph_generators.AdjacencyMatrix.

To demo this task, navigate to the main directory and run the following:
'''
$ python demo.py --config=spriteworld_physics.configs.star_system \
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

    # Factor distribution for the fixed center star
    center_factors = distribs.Product([
        distribs.Discrete('x', [0.5]),
        distribs.Discrete('y', [0.5]),
        distribs.Discrete('shape', ['circle']),
        distribs.Discrete('scale', [0.15]),
        distribs.Discrete('c0', [3.]),
        distribs.Discrete('c1', [1.]),
        distribs.Discrete('c2', [1.]),
        distribs.Continuous('mass', 1, 3),
    ])

    center_sprite_gen = generate_sprites.generate_sprites(
        center_factors, num_sprites=1)

    # Factor distributions for the orbiting sprites
    orbit_factors = distribs.Product([
        distribs.Continuous('x', 0.1, 0.9),
        distribs.Continuous('y', 0.1, 0.9),
        distribs.Discrete('shape', ['star_4', 'star_5', 'star_6']),
        distribs.Discrete('scale', [0.08]),
        distribs.Continuous('c0', 0, 1),
        distribs.Continuous('c1', 0.5, 1.),
        distribs.Discrete('c2', [1.]),
        distribs.Continuous('x_vel', -0.03, 0.03),
        distribs.Continuous('y_vel', -0.03, 0.03),
        distribs.Discrete('mass', [1]),
    ])

    orbit_sprite_gen = generate_sprites.generate_sprites(
        orbit_factors, num_sprites=4)

    sprite_gen = sprite_generators.chain_generators(
        center_sprite_gen, orbit_sprite_gen)

    force = forces.Gravity(gravity_constant=-0.0001,
                           distance_for_max_force=0.05)
    adjacency_matrix = {
        (0, 1): force,
        (0, 2): force,
        (0, 3): force,
        (0, 4): force,
    }

    graph_generator = graph_generators.AdjacencyMatrix(
        adjacency_matrix=adjacency_matrix, symmetric=False)

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
