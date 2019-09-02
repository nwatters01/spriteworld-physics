"""Sprite object for Spriteworld with physics."""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
from spriteworld import sprite
import numpy as np

FACTOR_NAMES = (
    'x',  # x-position of sprite center-of-mass (float)
    'y',  # y-position of sprite center-of-mass (float)
    'shape',  # shape (string)
    'angle',  # angle in degrees (scalar)
    'scale',  # size of sprite (float)
    'c0',  # first color component (scalar)
    'c1',  # second color component (scalar)
    'c2',  # third color component (scalar)
    'x_vel',  # x-component of velocity (float)
    'y_vel',  # y-component of velocity (float)
    'mass',  # mass (float)
)


class Sprite(sprite.Sprite):
    """Sprite class.

    Sprites are simple shapes parameterized by a few factors (position, shape,
    angle, scale, color, velocity). They are the building blocks of Spriteworld,
    so every Spriteworld environment state is simple a collection of sprites.
    """

    def __init__(self,
                 x=0.5,
                 y=0.5,
                 shape='square',
                 angle=0,
                 scale=0.1,
                 c0=0,
                 c1=0,
                 c2=0,
                 x_vel=0.0,
                 y_vel=0.0,
                 mass=1.0):
        """Construct sprite.

        Args:
            x: Float in [0, 1]. x-position.
            y: Float in [0, 1]. y-position.
            shape: String. Shape of the sprite. Must be a key of
                spriteworld.constants.SHAPES.
            angle: Int. Angle in degrees.
            scale: Float in [0, 1]. Scale of the sprite, from a point to the
                area of the entire frame. This scales linearly with respect to
                sprite width, hence with power 1/2 with respect to sprite area.
            c0: Scalar. First coordinate of color.
            c1: Scalar. Second coordinate of color.
            c2: Scalar. Third coordinate of color.
            x_vel: Float. x-velocity.
            y_vel: Float. y-velocity.
            mass: Float. Mass.
        """
        super(Sprite, self).__init__(x=x,
                                     y=y,
                                     shape=shape,
                                     angle=angle,
                                     scale=scale,
                                     c0=c0,
                                     c1=c1,
                                     c2=c2,
                                     x_vel=x_vel,
                                     y_vel=y_vel)
        self._velocity = np.array([x_vel, y_vel])
        self._mass = mass

    def update_position(self, bounce_off_walls=False, delta_t=1.):
        """Bounce off walls if out of frame.

        Args:
            bounce_off_walls: Bool. Whether to make the sprite bounce of walls
                if its position is out of the frame.
            delta_t: Float. Should be in [0, 1]. Time bin corresponding to this
                update, hence multiplied by the velocity when updating the
                position.
        """
        if bounce_off_walls:
            for coord in (0, 1):
                if ((self.position[coord] < 0 and self.velocity[coord] < 0) or
                        (self.position[coord] > 1 and self.velocity[coord] > 0)):
                    self.velocity[coord] *= -1
        # We set keep_in_frame to False because we are making the sprites bounce
        # off walls. keep_in_frame=True would make them slide along the walls.
        self.move(delta_t * self.velocity, keep_in_frame=False)

    def update_velocity(self, delta_velocity):
        self._velocity += delta_velocity

    @property
    def mass(self):
        return self._mass

    @property
    def factors(self):
        factors = collections.OrderedDict()
        for factor_name in FACTOR_NAMES:
            factors[factor_name] = getattr(self, factor_name)
        return factors
