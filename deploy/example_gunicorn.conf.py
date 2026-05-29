workers = 2
threads = 2
wsgi_app = "WebHost:get_app()"
# Import WSGI app once in the master before forking workers to download worlds.
preload_app = True

# Recycle each worker after this many requests to bound slow memory growth from
# any per-request leak (app code or a C-extension). With preload_app=True the
# replacement re-forks from the warm master, so recycling is cheap. Jitter keeps
# the workers from recycling in lockstep.
max_requests = 1000
max_requests_jitter = 200
# Let in-flight requests finish when a worker is recycled, reloaded, or shut down.
graceful_timeout = 30

accesslog = "-"
access_log_format = (
    '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
worker_class = "gthread"  # "sync" | "gthread"
forwarded_allow_ips = "*"
loglevel = "info"

"""
You can programatically set values.
For example, set number of workers to half of the cpu count:

import multiprocessing

workers = multiprocessing.cpu_count() / 2
"""
