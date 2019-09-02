"""Start demo for physics in Spriteworld.

This demo opens a matplotlib figure and plays the environment as a video.

To play a config, run this on the config:
```bash
python run_demo.py --config=$path_to_task_config$
```

If the config's colors are defined in RGB space instead of HSV space, add the
flag `--hsv_colors=False`.

If you would like to use a mode other than "train", add the flag
`--mode=$mode$`.

This file is modified from run_demo.py in the Spriteworld library, available
from https://github.com/deepmind/spriteworld/.
"""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
import importlib
from spriteworld import renderers
from spriteworld_physics import physics_environment

import matplotlib
matplotlib.use('TKAgg', force=True)
import matplotlib.pylab as plt

FLAGS = flags.FLAGS
flags.DEFINE_string('config', 'spriteworld_physics.configs.springs',
                    'Module name of task config to use.')
flags.DEFINE_string('mode', 'train', 'Mode, "train" or "test"]')
flags.DEFINE_boolean('hsv_colors', True,
                     'Whether the config uses HSV as color factors.')
flags.DEFINE_integer('render_size', 256,
                     'Height and width of the output image.')
flags.DEFINE_integer('anti_aliasing', 10, 'Renderer anti-aliasing factor.')
flags.DEFINE_float('pause_between_frames', 0.001, 'Pause between frames.')


class DemoUI(object):
    """Class for visualising the environment based on Matplotlib."""

    def __init__(self):
        plt.ion()
        self._fig = plt.figure(
            figsize=(6, 6), num='Spriteworld', facecolor='white')
        self._ax_image = plt.subplot(111)
        self._ax_image.axis('off')

    def _draw_observation(self, image):
        """Draw the latest observation."""
        self._ax_image.clear()
        self._ax_image.imshow(image, interpolation='none')
        self._ax_image.set_xticks([])
        self._ax_image.set_yticks([])

    def update(self, timestep):
        """Update the visualisation with the latest timestep."""
        self._draw_observation(timestep.observation['image'])
        plt.show(block=False)
        plt.pause(FLAGS.pause_between_frames)


def main(_):
    # Load and adjust environment config
    config = importlib.import_module(FLAGS.config)
    config = config.get_config(FLAGS.mode)
    config['renderers'] = {
        'image':
            renderers.PILRenderer(
                image_size=(FLAGS.render_size, FLAGS.render_size),
                color_to_rgb=renderers.color_maps.hsv_to_rgb
                if FLAGS.hsv_colors else None,
                anti_aliasing=FLAGS.anti_aliasing),
    }
    env = physics_environment.PhysicsEnvironment(**config)
    demo = DemoUI()

    # Run the environment in a loop
    timestep = env.reset()
    demo.update(timestep)
    while True:
        timestep = env.step()
        demo.update(timestep)


if __name__ == '__main__':
    app.run(main)
