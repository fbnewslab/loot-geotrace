loot-geotrace
=============

restful traceroute plus geoip 

    curl  127.0.0.1:61080/geotrace/www.google.com,HOST2,HOST3,...
    -> 

```json
    {
	"routes": [
	    {
		"dest_host": "cern.ch", 
		"dest_ip": "137.138.144.169", 
		"hops": [
		    ...HOP1, 
                    ...HOP2,...
		    {
			"geo": {
			    "continent": "EU", 
			    "country": "CH", 
			    "location": [
				46.1956, 
				6.1481
			    ], 
			    "subdivisions": [
				"GE"
			    ], 
			    "timezone": "Europe/Zurich"
			}, 
			"ip": "137.138.144.169"
		    }
	    ]},
	    { "dest_host": HOST2,
	    ...
	    }
       ]
    }
```

## INSTALL

pip install -r requirements.txt
pip install http://www.secdev.org/projects/scapy/files/scapy-latest.tar.gz

emacs config.py 

python geotrace.py
