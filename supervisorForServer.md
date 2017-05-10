#### INSTALL

```
$ sudo apt-get install supervisor
```

#### SETUP


1. create configuration file

```
$ sudo touch /etc/supervisor/conf.d/miraz.conf
$ sudo nano /etc/supervisor/conf.d/miraz.conf
```


2. paste configuration

```
[program:miraz_site]
process_name=MIRAZ-DJANGO-%(process_num)s
command=/home/miznat/venv_new/bin/uwsgi --ini /home/miznat/ht_web.ini
environment=PATH="/home/miznat/venv_new/bin/"
directory=/home/miznat/ht_web/
autostart=true
autorestart=true
stderr_logfile=/var/log/miraz-supervisor.err.log
stdout_logfile=/var/log/miraz-supervisor.out.log
```

3. init new configuration and start service

```
supervisorctl reread
supervisorctl update
```

4. go to supervisor and check service

```
sudo supervisorctl
```

5. restart all supervisor services if need

```
sudo supervisorctl restart all
```
