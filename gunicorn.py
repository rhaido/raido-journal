import os
 
def numCPUs():
  if not hasattr(os, "sysconf"):
    raise RuntimeError("No sysconf detected.")
  return os.sysconf("SC_NPROCESSORS_ONLN")
  
bind = "127.0.0.1:9000"
workers = 4
backlog = 128 
#worker_class ="sync"
worker_class =  "gevent"
debug = True
#loglevel = "debug"
daemon = True
#daemon = False
pidfile ="/tmp/gunicorn.pid"
errorlog ="/tmp/gunicorn.log"

