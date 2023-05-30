bind = "0.0.0.0:8000"
workers = 3
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 20
threads = 1
chdir = "/app/"
capture_output = True
