"""
Helper script for automating multiple scans back to back.
"""

import os
import time
import sys

# Coverage guided list of domains (not in order)
hosts = [
    'anticommunism.miraheze.org',
    'citizenpowerforchina.org',
    'epochtimes.com',
    'falundafa.org',
    'www.hrw.org',
    'www.youporn.com',
    'www.pornhub.com',
    'www.bittorrent.com',
    'www.roxypalace.com',
    'plus.google.com',
    'www.survive.org.uk'
]

if len(sys.argv) < 2:
    print("Usage: %s <output_filename>" % __file__)
    exit()

config = sys.argv[1]
gigbit = sys.argv[2]
path = "scan/%s" % config
os.makedirs(path,exist_ok=True)
try:
    for host in hosts:
        print("*" * 100)
        print("INITIATING SCAN FOR %s" % host)
        cmd = """
        sed "s/#define HOST .*/#define HOST \\\"%s\\\"/g" src/probe_modules/module_forbidden_scan.c > src/probe_modules/.backup
        """ % host
        print(cmd)
        os.system(cmd)
        time.sleep(1)
        os.system("mv src/probe_modules/.backup src/probe_modules/module_forbidden_scan.c")
        time.sleep(1)
        if os.path.exists("%s/%s.csv" % (path, host)):
            os.remove("%s/%s.csv" % (path, host))
        os.system("cmake . && make -j8 && sudo src/zmap -M forbidden_scan -p 80 -w ./cn.zone -f \"saddr,payloadlen,flags,validation_type\" -o %s/%s.csv -O csv -B %sM" % (path, host, gigbit))
        print("Scan for %s finished" % host)
        print("Sleeping for 60 seconds before next scan.")
        time.sleep(60)
except KeyboardInterrupt:
    print("Exiting")
