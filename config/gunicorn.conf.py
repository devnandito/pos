import multiprocessing

bind = 'unix:/var/www/envapp/.pos/run/gunicorn.sock'
workers = multiprocessing.cpu_count() * 2