"""Collection of pairwise forces for physics in Spriteworld."""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import numpy as np
import six


@six.add_metaclass(abc.ABCMeta)
class AbstractForce(object):
    """Abstract class from which all distributions should inherit."""

    def get_diff_dist_force_direction(self, acting_sprite, receiving_sprite):
        diff = receiving_sprite.position - acting_sprite.position
        dist = np.linalg.norm(diff)
        force_direction = diff / dist
        return diff, dist, force_direction

    @abc.abstractmethod
    def apply_force(self, acting_sprite, receiving_sprite, force_multiplier=1.):
        """Apply force from acting_sprite to receiving_sprite.
        
        Args:
            acting_sprite: Instance of sprite.Sprite.
            receiving_sprite: Instance of sprite.Sprite.
            force_multiplier: Coefficient to multiply to the force. Typically
                used to normalize the force when it is being applied multiple
                times per environment step.
        """

    @abc.abstractmethod
    def metadata(self):
        """Return dictionary containing force metadata."""


class NoForce(AbstractForce):
    """Applies no force to sprites."""

    def __init__(self):
        pass

    def apply_force(self, *unused_args, **unused_kwargs):
        pass

    def metadata(self):
        return {'force': 'NoForce'}


class Spring(AbstractForce):
    """Applies spring force according to Hooke's Law."""

    def __init__(self, spring_constant, spring_equilibrium):
        """Construct spring force.

        Args:
            spring_constant: Non-negative scalar. Spring constant in Hooke's
                Law.
            spring_equilibrium: Non-negative scalar. Resting equilibrium of the
                spring.
        """
        self._spring_constant = spring_constant
        self._spring_equilibrium = spring_equilibrium

    def apply_force(self, acting_sprite, receiving_sprite, force_multiplier=1.):
        _, dist, force_direction = self.get_diff_dist_force_direction(
            acting_sprite, receiving_sprite)
        force_magnitude = -1. * force_multiplier * self._spring_constant * \
            (dist - self._spring_equilibrium)
        acceleration = force_magnitude * force_direction / receiving_sprite.mass
        receiving_sprite.update_velocity(acceleration)

    def metadata(self):
        return {'force': 'Spring',
                'spring_constant': self._spring_constant,
                'spring_equilibrium': self._spring_equilibrium}


class Gravity(AbstractForce):
    """Applies gravitational force according to Newton's Law.
    
    This can also be used to implement magnetic repulsion in the style of
    Coulomb's Law, except the sprites' charges are the same as as their masses.
    """
    def __init__(self, gravity_constant, distance_for_max_force=0.01):
        """Construct gravitational force.

        Args:
            gravity_constant: Scalar. Gravitational constant. May be negative to
                implement a repulsive force.
            distance_for_max_force: Scalar. Distance corresponding to the
                maximum allowed force. Sprites nearer than this distance will
                have a force as if there were at this distance. This is
                important to avoid acceleration/velocity explosion if sprites
                get too close.
        """
        self._gravity_constant = gravity_constant
        self._distance_for_max_force = distance_for_max_force

    def apply_force(self, acting_sprite, receiving_sprite, force_multiplier=1.):
        _, dist, force_direction = self.get_diff_dist_force_direction(
            acting_sprite, receiving_sprite)
        dist = max(dist, self._distance_for_max_force)
        force_magnitude = (
            force_multiplier * self._gravity_constant * acting_sprite.mass *
            receiving_sprite.mass) / (dist * dist)
        acceleration = force_magnitude * force_direction / receiving_sprite.mass
        receiving_sprite.update_velocity(acceleration)

    def metadata(self):
        return {'force': 'Gravity', 'gravity_constant': self._gravity_constant}


class SymmetricShellCollision(AbstractForce):
    """Applies collisions.

    These collisions are not physically realistic with respect to the sprites'
    shapes, but instead are implemented as an invisible rigid circular shell
    around each sprite.

    This force is also symmetric, so when creating a force graph, be sure to
    never have a collision both in entry (i, j) and in entry (j, i). For
    example, use graph_generators.LowerTriangular for all-to-all collisions.
    """
    def __init__(self, shell_radius):
        self._shell_radius = shell_radius

    def apply_force(self, acting_sprite, receiving_sprite, force_multiplier=1.):
        del force_multiplier # Unused

        diff, dist, _ = self.get_diff_dist_force_direction(
            acting_sprite, receiving_sprite)

        # Don't bounce if not within 2 * shell_radius
        if dist > 2 * self._shell_radius:
            return

        total_momentum = (acting_sprite.mass * acting_sprite.velocity +
                          receiving_sprite.mass * receiving_sprite.velocity)

        total_vel = (total_momentum /
                     (acting_sprite.mass + receiving_sprite.mass))

        acting_centered_vel = acting_sprite.velocity - total_vel
        receiving_centered_vel = receiving_sprite.velocity - total_vel

        # Don't bounce if sprites are moving away from each other. This likely
        # means that they have already bounced but have not yet moved outside
        # shell_radius.
        if np.dot(diff, acting_centered_vel) < 0:
            return

        # Compute the bounce and update sprite velocities
        normalized_diff = diff / dist
        acting_vel_update = (
            -2. * np.dot(normalized_diff, acting_centered_vel) *
            normalized_diff)
        acting_sprite.update_velocity(acting_vel_update)
        receiving_vel_update = (
            -2. * np.dot(normalized_diff, receiving_centered_vel) *
            normalized_diff)
        receiving_sprite.update_velocity(receiving_vel_update)

    def metadata(self):
        return {'force': 'ShellCollision', 'shell_radius': self._shell_radius}
