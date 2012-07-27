import os
 
def numCPUs():
  if not hasattr(os, "sysconf"):
    raise RuntimeError("No sysconf detected.")
  return os.sysconf("SC_NPROCESSORS_ONLN")
  
bind = "0.0.0.0:9000"
workers = numCPUs()
backlog = 128 
#worker_class ="sync"
worker_class =  "gevent"
debug = True
daemon = True
pidfile ="/tmp/gunicorn.pid"
errorlog ="/tmp/gunicorn.log"

