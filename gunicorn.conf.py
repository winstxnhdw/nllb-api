# pylint: skip-file

from server.config import Config

wsgi_app = 'server:initialise()'
reload = False
accesslog = '-'
limit_request_fields = 1
limit_request_field_size = 2048
preload_app = True
bind = f'0.0.0.0:{Config.server_port}'
workers = Config.worker_count
worker_class = 'uvicorn.workers.UvicornWorker'
timeout = 300
