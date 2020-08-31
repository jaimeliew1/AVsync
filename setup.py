# https://python-packaging.readthedocs.io
from setuptools import setup

setup(name                 = 'AVsync',
      version              = '0.1',
      description          = 'Synchronizes video and audio files in Python',
      #url                  =
      author               = 'Jaime Liew',
      author_email         = 'jaimeliew1@gmail.com',
      packages             = ['avsync'],
      install_requires     = ['moviepy'],
      entry_points         = {
        'console_scripts': ['avsync=avsync.cli:cli']},
)
