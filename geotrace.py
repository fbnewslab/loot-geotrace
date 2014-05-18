#!/usr/bin/env python                                                                  
# coding=utf-8                                                                         

from config import Config

if "gevent" in Config.mode:
    # monkey patch very early, so we dont miss any modules (e.g. bottle) that need it  
    import gevent.monkey; gevent.monkey.patch_all()
    import gevent, gevent.coros 

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("geotrace")

import subprocess, json
from pprint import pprint 

import bottle
from bottle import route, request, response, abort, error, auth_basic

from geoip import geolite2

from memoize import memoize


#def valid_user(u,p):
#    auth = getattr(Config, "auth", None)
#    if not auth:
#        return True  # public if no auth config!                                       
#    return (auth.get(u) == p)



max_concurrent_traces = None
if "gevent" in Config.mode:
    max_concurrent_traces = gevent.coros.Semaphore(value=getattr(Config, "max_concurrent_traces", 1))


@route('/geotrace/<hosts>', method='GET')
def geotrace(hosts):
    if max_concurrent_traces is not None:
        with max_concurrent_traces:
            return _trace(hosts)
    else:
        return _trace(hosts)

@memoize(timeout=15*60)
def _trace(hosts):
    hosts = hosts.split(",")
    if not hosts:
        abort(400)
    hosts = list(set(hosts)) # unique
    
    cmd = ["/usr/bin/sudo", "./ptraceroute.py"] + hosts 
    try:
        out = subprocess.check_output(cmd)
        data = json.loads(out)
    except subprocess.CalledProcessError:
        abort(500, "traceroute error")

    lookups, trace = data["lookups"], data["trace"]
    
    result = dict(routes=[])
    for hostname, ip in lookups.items():
        if ip not in trace:
            logger.warn(u"ip {} for hostname {} not found in trace".format(ip, hostname))
            continue
        hops = trace[ip]
        route = dict(dest_ip=ip, dest_host=hostname, hops=[])
        for idx in sorted(hops.keys(), key=int):
            hop_ip,stop = hops[idx]
            hop = dict(ip=hop_ip)
            hop = add_geo_info(hop)
            route["hops"].append(hop)
        result["routes"].append(route)

    return result  # auto json
        

def add_geo_info(hop):
    match = geolite2.lookup(hop["ip"])
    if match is not None:
        hop["geo"] = geo = dict((k,getattr(match, k)) for k in ["country", "continent", "timezone", "location"])
        geo["subdivisions"] = list(match.subdivisions)  # convert from frozenset
    return hop



@route('/ping', method='GET', name="ping")
def ping():
    return "pong"


@error(500)
def error500(error):
    logger.error("Error 500: %r"%(error,))



if __name__ == '__main__':
    config = Config
    if config.mode == "devel":
        bottle.debug(True)
        bottle.run(reloader=True, host=config.host, port=config.port)
    elif config.mode == "devel-gevent":
        bottle.run(host=config.host, port=config.port, server='gevent')
