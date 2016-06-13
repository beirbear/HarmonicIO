from setuptools import setup

setup(name='harmonicIO',
      version='0.1.0',
      install_requires=['falcon'],
      packages=['data_source'],
      entry_points={
          'console_scripts': [
              'DataSource = data_source.__main__:main',
              'data_source = data_source.__main__:main',
          ]
      }
      )
