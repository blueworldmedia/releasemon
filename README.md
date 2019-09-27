# Releasemon

Supervisor plugin to watch a build version file and restart programs on update

## Overview

Releasemon is designed to actively monitor a known version file for changes, and if an update occurs restart supervisor managed programs. 

It was inspired by Tim Schumacher's superfsmon script, but is designed for automatically reload changes in a hands-off production environment and includes some addtional functionality.

Specifically, releasemon will:

- Monitor a given version file on the filesystem
- If a change is detected, it will re-read the version and see if it has been updated
- If it has, it will restart the supervisor programs or groups as required

In addition, releasemon will:

- Allow for pre-restart and post-restart scripts to be executed
- Allow only 'RUNNING' processes to restart (to avoid multiple restarts on STARTING processes)
- Limit the number of files being monitored to only one (limiting inotify resources needed) 

Releasemon uses Supervisor's XML-RPC API. Your
`supervisord.conf` file must have a valid `[unix_http_server]` or
`[inet_http_server]` section and a `[rpcinterface:supervisor]` section.
If you are able to control your Supervisor instance with `supervisorctl`, you
have already have this coonigured.

To restart your celery workers on changes in the `/app/devops` directory your
`supervisord.conf` could look like this.

    [program:celery]
    command=celery -A devops.celery worker --loglevel=INFO --concurrency=10

    [program:superfsmon]
    command=releasemon /appdir/.version celery

You can use multiple instances of Releasemon to control different programs.

## Installation

### Python 2

    pip install superfsmon

### Python 3

This script requires Supervisor which [is not yet available for Python
3][Supervisor Python 3]. To be able to install superfsmon without errors you
need to install the development version of Supervisor from the GitHub
repository first. The development version may not work reliably, don't use it
in production.

    pip install git+https://github.com/Supervisor/supervisor
    pip install superfsmon

[Supervisor Python 3]: https://github.com/Supervisor/supervisor/issues/510


## Command Line Arguments

    usage: releasemon [-h] [-e FLAG] [--disable [FLAG]]
                      [-rd SECONDS] [-fd SECONDS] [--running-only] 
                       [-g GROUP] [-a]
                      PATH [PROG [PROG ...]]

    Supervisor plugin to watch a directory and restart programs on changes

    optional arguments:
      -h, --help            show this help message and exit
      -e FLAG, --enable FLAG
                            disable functionality if flag is not set
      --disable [FLAG]      disable functionality if flag is set
      -rd, --random-delay   random delay in seconds prior to restarting after version change
      -fd, --fixed-delay    fixed delay in seconds prior to restarting after version change

    additional tasks:
      -pre, --pre-restart   system command to run prior to restarting programs
      -post, --post-restart system command to run after restarting programs
      
    directory monitoring:
      FILEPATH              full path to version file to watch for changes
            
    programs:
      PROG                  supervisor program name to restart
      -g GROUP, --group GROUP
                            supervisor group name to restart
      -a, --any             restart any child of this supervisor

## Examples

Restart Supervisor program 'app':

    command=releasemon /appdir/.version app

Restart Supervisor program 'app' then run a post-update script:

    command=releasemon --pre-restart "echo 'POST ROTATE SCRIPT'" /appdir/.version app

Restart all Supervisor programs in the `workers` group after 10 seconds:

    command=releasemon --fixed-delay 10 -g workers /appdir/.version

Restart all Supervisor programs in the `workers` group after a random delay between 0 and 60 seconds:

    command=releasemon --random-delay 10 -g workers /appdir/.version


Disable functionality using an environment variable:

    command=releasemon /appdir/.version app1 -e %(ENV_CELERY_AUTORELOAD)s

## Known Issues

[Watchdog Issue]: https://github.com/gorakhargosh/watchdog/issues/442

## Inspired by

Superfsmon by Tim Schumacher
https://github.com/timakro/superfsmon

## License

Copyright (C) 2019 James Cundle

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent per‐mitted by law.