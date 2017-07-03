import os
import sys
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from multiprocessing import Process, Queue
from functools import partial

q = Queue()

def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    rc = nmproc.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    print(type(nmproc.stdout))

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))
    urls = (f'http://{host.address}:{service.port}' for host in parsed.hosts if host.is_up() for service in host.services if service.open())
    for url in urls:
        q.put(url)

scan = partial(do_scan, options='-sV')

def saveResult():
    with open('result.txt', 'a') as f:
        while True:
            url = q.get()
            print(url)
            f.write(url+'\n')

if __name__ == "__main__":
    ips = (ip.strip() for ip in open('./ips.txt'))
    p = Process(target=saveResult)
    p.start()
    ps = []
    for ip in ips:
        p = Process(target=scan, args=(ip, ))
        p.start()
        ps.append(p)
    for i in ps:
        print(i)
        i.join()
    p.join()
