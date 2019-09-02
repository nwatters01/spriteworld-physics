"""Generate gif from physics in Spriteworld config.

This script runs the environment on a config in writes a video of the image
observations.

To run this script a config, run this on the config:
```bash
python generate_gif.py --config=$path_to_task_config$
```

If the config's colors are defined in HSV space, add the flag
`--hsv_colors=True`.

If you would like to use a mode other than "train", add the flag
`--mode=$mode$`.
"""

# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from absl import logging
import imageio
import importlib
import os
from spriteworld import renderers
from spriteworld_physics import physics_environment

FLAGS = flags.FLAGS
flags.DEFINE_string('config', 'spriteworld_physics.configs.collisions',
                    'Module name of task config to use.')
flags.DEFINE_string('mode', 'train', 'Mode, "train" or "test"]')
flags.DEFINE_boolean('hsv_colors', True,
                     'Whether the config uses HSV as color factors.')
flags.DEFINE_integer('render_size', 256,
                     'Height and width of the output image.')
flags.DEFINE_integer('anti_aliasing', 10, 'Renderer anti-aliasing factor.')
flags.DEFINE_integer(
    'num_episodes', 5, 'Number of episodes to run for the gif.')
flags.DEFINE_float('fps', 8, 'Number of frames per second for the gif.')
flags.DEFINE_string(
    'gif_path_head',
    '~/Desktop/grad_school_research/shaul_spriteworld/gifs',
    'Head of the file path to write the gif to.')
flags.DEFINE_string(
    'gif_path_tail',
    'collisions.gif',
    'Tail of the file path to write the gif to.')


def main(_):
    logging.info('Generating gif for config {}'.format(FLAGS.config))
    
    gif_path = os.path.join(FLAGS.gif_path_head, FLAGS.gif_path_tail)
    if gif_path[0] == '~':
        gif_path = os.path.join(os.path.expanduser('~'), gif_path[2:])
    if os.path.isfile(gif_path):
        should_continue = input('Path {} to write gif to already exists. '
                                'Overwrite the existing file? (y/n)')
        if should_continue != 'y':
            logging.info('You pressed {}, not "y", so terminating '
                         'program.'.format(should_continue))
            return
        else:
            logging.info('You pressed "y". Overwriting existing file.')

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

    # Run the environment in a loop
    duration_per_frame = 1. / FLAGS.fps
    timestep = env.reset()
    images = []
    episodes_generated = 0
    while episodes_generated < FLAGS.num_episodes:
        images.append(timestep.observation['image'])
        if timestep.last():
            episodes_generated += 1
            logging.info('Generated {} of {} episodes'.format(
                episodes_generated, FLAGS.num_episodes))
        timestep = env.step()

    logging.info('Writing gif to file {}'.format(gif_path))
    imageio.mimsave(gif_path, images, duration=duration_per_frame)


if __name__ == '__main__':
    app.run(main)
