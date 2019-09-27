from setuptools import setup

setup(name='releasemon',
      version='1.0.0',
      license='GPLv3',
      description='Supervisor plugin to watch a build version file and restart '
                  'programs on update',
      author='James Cundle',
      author_email='james@blueworldmedia.com',
      url='https://github.com/blueworldmedia/releasemon',
      install_requires=['supervisor', 'watchdog'],
      scripts=['releasemon']
      )
