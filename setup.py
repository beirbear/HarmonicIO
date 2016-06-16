from setuptools import setup

setup(name='harmonicIO',
      version='0.1.0',
      install_requires=['falcon', 'urllib3'],
      packages=['data_source', 'master', 'worker'],
      entry_points={
          'console_scripts': [
              'data_source = data_source.__main__:main',
              'master = master.__main__:main',
              'worker = worker.__main__:main',
          ]
      }
      )
