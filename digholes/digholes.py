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
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
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
    ps = []
    p1 = Process(target=preprocessing.main, args=(settings_pre,))
    p2 = Process(target=scanner.main, args=(settings_scan,))
    p3 = Process(target=crawler.main, args=(settings_crawl,))
    logger.info("启动各子进程")
    for p in p1, p2, p3:
        p.daemon = True
        p.start()
        ps.append(p)
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
