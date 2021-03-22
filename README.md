# Releasemon

Supervisor plugin to watch a build version file and restart programs on update

## Overview

Releasemon is designed to actively monitor a known version file for changes, and if an update occurs restart supervisor managed programs. 

It was specifically written to restart Laravel queues on deployment when **the contents** of a known version or timestamp file has changed. 

Originally inspired by Tim Schumacher's superfsmon script, releasemon is optimized to restart applications only when a specific file is seen to have updates made to its contents. This is more resource friendly as it won't keep file notification handles open for every file in a given directory (e.g all your repository source files) which can cause inotify limits to be hit on large filesystems. Notably, simply updating the timestamp (e.g. through an rsync) will NOT force restart, meaning you can limit restarts based on explicit file updates and not through unreleated filesystem changes.

realeasmon also adds some new functionality such as random offsets on restart times (which can be useful for distributing load spikes).


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

To restart your Laravel worker when the contents of `/appdir/.version` is updated,
your `supervisord.conf` might look like this.

    [program:laravel-worker]
    command=php /home/forge/app.com/artisan queue:work sqs --sleep=3 --tries=3 --max-time=3600

    [program:releasemon]
    command=releasemon /appdir/.version laravel-worker

You can use multiple instances of Releasemon to control different programs.

## Installation

### Python 2 and 3

    pip install releasemon


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

The following examples assume you make updates to the file `/appdir/.version` on each release:

Restart Supervisor program 'app':

    [program:releasemon]
    command=releasemon /appdir/.version app

Restart Supervisor program 'app' then run a post-update script:

    [program:releasemon]
    command=releasemon --pre-restart "echo 'POST ROTATE SCRIPT'" /appdir/.version app

Restart all Supervisor programs in the `workers` group after 10 seconds:

    [program:releasemon]
    command=releasemon --fixed-delay 10 -g workers /appdir/.version

Restart all Supervisor programs in the `workers` group after a random delay between 0 and 60 seconds:

    [program:releasemon]
    command=releasemon --random-delay 60 -g workers /appdir/.version

Restart all Supervisor programs

    [program:releasemon]
    command=releasemon -a /appdir/.version app

Disable functionality using an environment variable:

    [program:releasemon]
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
