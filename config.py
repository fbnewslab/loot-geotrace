
class Config(object):
    mode = "devel-gevent"  # "devel" # "devel" 
    host = "0.0.0.0" # "127.0.0.1"
    port = 61080

    # auth = { "u": "p"}

    max_concurrent_traces = 5  # only with gevent
