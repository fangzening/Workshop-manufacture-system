# gunicorn configuration file

bind = '0.0.0.0:8000'
reload = True
deamon = True
accesslog = '-'
errorlog = '-'
loglevel = 'info'