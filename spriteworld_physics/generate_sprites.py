"""This file re-implements spriteworld.sprite_generators.generate_sprites().

This is necessary only because spriteworld.sprite_generators.generate_sprites()
uses the spriteworld.sprite.Sprite as the sprite constructor, whereas we would
like to use the sprite.Sprite constructor in this codebase.

This file is modified from sprite_generators.py in the Spriteworld library,
available from https://github.com/deepmind/spriteworld/.
"""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from spriteworld_physics import sprite


def generate_sprites(factor_dist, num_sprites=1):
  """Create callable that samples sprites from a factor distribution.

  Args:
    factor_dist: The factor distribution from which to sample. Should be an
      instance of factor_distributions.AbstractDistribution.
    num_sprites: Int or callable returning int. Number of sprites to generate
      per call.

  Returns:
    _generate: Callable that returns a list of Sprites.
  """

  def _generate():
    n = num_sprites() if callable(num_sprites) else num_sprites
    sprites = [sprite.Sprite(**factor_dist.sample()) for _ in range(n)]
    return sprites

  return _generate