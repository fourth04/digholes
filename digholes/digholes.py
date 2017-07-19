from . import preprocessing
from . import scanner
from . import crawler
from .config import Config
import logging
from multiprocessing import Process
import os
import signal
import time
import argparse
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def terminate_handler(sig_num, addtion):
    logger.error('current pid is %s, group id is %s' % (os.getpid(), os.getpgrp()))
    os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)

def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('config', action='store', help='config file path')
    args = parser.parse_args()

    settings = Config.from_pyfile(args.config)
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

    settings_pre = settings.copy()
    settings_pre['SCHEDULER_DUPEFILTER_KEY'] = settings.get('SCHEDULER_DUPEFILTER_KEY_PRE', 'digholes:dupefilter')
    settings_pre['SCHEDULER_QUEUE_KEY'] = settings.get('SCHEDULER_QUEUE_KEY_PRE', 'digholes:queue_ip_pool')

    settings_scan = settings.copy()
    settings_scan['SCHEDULER_QUEUE_IN_KEY'] = settings.get('SCHEDULER_QUEUE_IN_KEY_SCAN', 'digholes:queue_ip_pool')
    settings_scan['SCHEDULER_QUEUE_OUT_KEY'] = settings.get('SCHEDULER_QUEUE_OUT_KEY_SCAN', 'digholes:queue_url_pool')

    settings_crawl = settings.copy()
    settings_crawl['SCHEDULER_QUEUE_IN_KEY'] = settings.get('SCHEDULER_QUEUE_IN_KEY_CRAWL', 'digholes:queue_url_pool')
    settings_crawl['SCHEDULER_QUEUE_OUT_KEY'] = settings.get('SCHEDULER_QUEUE_OUT_KEY_CRAWL ', 'digholes:queue_response_pool')

    num_scan_host_processes = settings.get('NUM_SCAN_HOST_PROCESSES', 1)

    ps = []
    for _ in range(num_scan_host_processes):
        ps.append(Process(target=scanner.main, args=(settings_scan,), name=f'scanner_{_}'))
    ps.append(Process(target=preprocessing.main, args=(settings_pre,), name='preprocessing'))
    ps.append(Process(target=crawler.main, args=(settings_crawl,), name='crawler'))

    for p in ps:
        p.daemon = True
        p.start()
        logger.info(f'启动进程：{p.name}，进程ID：{p.pid}')
    #  解决孤儿进程问题
    signal.signal(signal.SIGTERM, terminate_handler)
    #  当子进程挂了之后自动重启
    while True:
        for i, p in enumerate(ps):
            if not p.is_alive():
                logger.error('{} occured error, trying to reboot it'.format(p.name))
                ps[i] = Process(target=p._target, args=p._args, daemon=p.daemon, name=p._name)
                ps[i].start()
        time.sleep(60*5)
    for p in ps:
        p.join()

if __name__ == "__main__":
    main()
