Mac OS X Installing Redis

```bash
brew install redis
```

Starting redis

```bash
$ ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist

```

Starting the celery manager
```bash
python manage.py task_manager
```

Starting celery beat workers
```bash
celery -A daedalus beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```


