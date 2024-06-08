import multiprocessing

bind = "127.0.0.1:8000"
backlog = 2048
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
timeout = 300
keepalive = 2

accesslog = "-"
access_log_format = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s"
