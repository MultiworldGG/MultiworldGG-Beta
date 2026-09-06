workers = 2
threads = 2
wsgi_app = "WebHost:get_app()"
# Import the app (and every installed world) once in the master so workers
# fork from it copy-on-write instead of each importing ~235 worlds.
preload_app = True


def when_ready(server):
    # Move the preloaded heap to the permanent generation before forking: a
    # gen-2 collection in a worker rewrites every tracked object's GC header
    # and would otherwise make the whole shared heap private to that worker.
    import gc
    gc.collect()
    gc.freeze()

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
