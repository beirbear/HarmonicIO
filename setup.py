from setuptools import setup

setup(name='harmonicIO',
      version='0.2.0',
      install_requires=['falcon', 'urllib3', 'docker'],
      packages=['stream_connector', 'master', 'worker'],
      entry_points={
          'console_scripts': [
              'stream_connector = stream_connector.__main__:main',
              'master = master.__main__:main',
              'worker = worker.__main__:main',
              'play = play.__main__:main'
          ]
      }
      )
