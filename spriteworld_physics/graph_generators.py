"""Collection of functions generating interaction graphs.

An interaction graph is a matrix (list of lists) of size
num_sprites x num_sprites. The (i, j) entry of an interaction graph contains a
force to be applied by sprite i on sprite j.

Since each episode may contain a different number of sprites and require a
different interaction graph, the classes in this file are interaction graph
generators and all have a generate_graph(sprites) method that is called each
episode reset and returns the interaction graph for the given spites.
"""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import six
import numpy as np
from spriteworld_physics import forces


@six.add_metaclass(abc.ABCMeta)
class AbstractGraphGenerator(object):
    """Abstract class from which all interaction graphs should inherit."""

    @abc.abstractmethod
    def generate_graph(self, sprites):
        """Return interaction graph given iterable of sprites."""


class FullyConnected(AbstractGraphGenerator):
    """Fully connected graph with a single force."""

    def __init__(self, force):
        """The same force is applied between all pairs of sprites.

        The diagonal of the generated graph contains force.NoForce instances, so
        that sprites do not exert force on themselves.

        Note that since this applies a force from sprite i to sprite j and from
        sprite j to sprite i, this class should not be used for symmetric forces
        (like forces.SymmetricShellCollision). Instead consider LowerTriangular.

        Args:
            force: Instance of forces.AbstractForce.
        """
        self._force = force

    def generate_graph(self, sprites):
        graph = [[self._force for _ in sprites] for _ in sprites]
        for i in range(len(sprites)):
            graph[i][i] = forces.NoForce
        return graph


class LowerTriangular(AbstractGraphGenerator):
    """Fully connected graph with a single force."""

    def __init__(self, force):
        """Construct lower triangular graph generator.

        The same force is applied between the sprite pairs (i, j) where i < j.

        The diagonal and upper triangular portion of the generated graph
        contains force.NoForce instances.

        Note that since this never applies a force both from sprite i to sprite
        j and  from sprite j to sprite i, it can be used with symmetric forces
        (like forces.SymmetricShellCollision).

        Args:
            force: Instance of forces.AbstractForce.
        """
        self._force = force

    def generate_graph(self, sprites):
        graph = [[forces.NoForce for _ in sprites] for _ in sprites]
        for i in range(len(sprites)):
            for j in range(i):
                graph[i][j] = self._force
        return graph


class AdjacencyMatrix(AbstractGraphGenerator):
    """Graph defined in adjacency matrix style.

    Warning: If the number of sprites changes across episodes, use care with
    this graph generator, since the adjacency matrix does not change. If any
    indices of the adjacency matrix are greater than the number of sprites,
    there will be an error.
    """

    def __init__(self, adjacency_matrix, symmetric=True):
        """Construct AdjacencyMatrix graph generator.

        Args:
            adjacency_matrix: Dictionary. Keys are tuples of indices (i, j) and
                values are forces. For each key, this class will generate the
                corresponding value's force between the key indices.
            symmetric. Bool. Whether to make forces symmetric.
        """
        self._adjacency_matrix = adjacency_matrix
        self._symmetric = symmetric

    def generate_graph(self, sprites):
        graph = [[forces.NoForce for _ in sprites] for _ in sprites]
        for pair, force in self._adjacency_matrix.items():
            if pair[0] >= len(sprites) or pair[1] >= len(sprites):
                raise ValueError(
                    'pair {} has an index greater than or equal to the number '
                    'of sprites {}'.format(pair, len(sprites)))
            graph[pair[0]][pair[1]] = force
            if self._symmetric:
                graph[pair[1]][pair[0]] = force
        return graph
