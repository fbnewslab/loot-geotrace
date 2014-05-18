#!./venv/bin/python 
import sys, json, socket
from scapy.all import traceroute, conf

lookups = dict((hostname, socket.gethostbyname(hostname)) for hostname in sys.argv[1:])
ips = filter(None, set(lookups.values())) # distinct, remove false

conf.verb = 0
res, unans = traceroute(ips, maxttl=30)

print json.dumps(dict(lookups=lookups, trace=res.get_trace()))

