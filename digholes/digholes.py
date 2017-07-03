import preprocessing
import scanner
import crawler
import logging
import conf
from utils import get_settings
from multiprocessing import Process
import os
import signal
import time


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def term(sig_num, addtion):
    logger.error('current pid is %s, group id is %s' % (os.getpid(), os.getpgrp()))
    os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)

def main(settings):
    """TODO: Docstring for main.
    :returns: TODO

    """
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    settings_pre = dict(
        SCHEDULER_DUPEFILTER_KEY = 'digholes:dupefilter',
        SCHEDULER_QUEUE_KEY = 'digholes:queue_ip_pool',
        **settings
    )
    settings_scan = dict(
        SCHEDULER_QUEUE_IN_KEY = 'digholes:queue_ip_pool',
        SCHEDULER_QUEUE_OUT_KEY = 'digholes:queue_url_pool',
        **settings
    )
    settings_crawl = dict(
        SCHEDULER_QUEUE_IN_KEY = 'digholes:queue_url_pool',
        SCHEDULER_QUEUE_OUT_KEY = 'digholes:queue_response_pool',
        **settings
    )
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
    signal.signal(signal.SIGTERM, term)
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
    settings = get_settings(conf)
    main(settings)
