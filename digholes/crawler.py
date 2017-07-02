import requests
from lxml.html import fromstring
from redisqueue.scheduler import PipeScheduler
from concurrent.futures import ThreadPoolExecutor
import logging
import re

import importlib
import six
import time
from redisqueue import connection

class Crawler(PipeScheduler):

    """从redis-queue中获取url，进行爬取，然后再存放到另一个redis-queue中"""

    def __init__(self, server,
                 persist=False,
                 flush_on_start=False,
                 queue_in_key='queue_in:%(timestamp)s' % {'timestamp': int(time.time())},
                 queue_in_cls='redisqueue.rqueues.FifoQueue',
                 queue_out_key='queue_out:%(timestamp)s' % {'timestamp': int(time.time())},
                 queue_out_cls='redisqueue.rqueues.FifoQueue',
                 idle_before_close=0,
                 serializer=None,
                 num_crawl_threads=10,
                 blacklist=r'',
                 whitelist=r'.*'):

        """Initialize scheduler.

        Parameters
        ----------
        blacklist : str
            网页标题过滤黑名单
        whitelist : str
            网页标题过滤白名单
        num_crawl_threads: int
            同时爬取网页内容的线程数
        """
        super().__init__(server, persist, flush_on_start, queue_in_key, queue_in_cls, queue_out_key, queue_out_cls, idle_before_close, serializer)
        self.num_crawl_threads = num_crawl_threads
        self.blacklist = re.compile(blacklist)
        self.whitelist = re.compile(whitelist)

    @classmethod
    def from_settings(cls, settings):
        kwargs = {
            'persist': settings.get('SCHEDULER_PERSIST', True),
            'flush_on_start': settings.get('SCHEDULER_FLUSH_ON_START', False),
            'queue_in_key': settings.get('SCHEDULER_QUEUE_IN_KEY', 'queue_in:%(timestamp)s' % {'timestamp': int(time.time())}),
            'queue_in_cls': settings.get('SCHEDULER_QUEUE_IN_CLASS', 'redisqueue.rqueues.FifoQueue'),
            'queue_out_key': settings.get('SCHEDULER_QUEUE_OUT_KEY', 'queue_out:%(timestamp)s' % {'timestamp': int(time.time())}),
            'queue_out_cls': settings.get('SCHEDULER_QUEUE_OUT_CLASS', 'redisqueue.rqueues.FifoQueue'),
            'idle_before_close': settings.get('SCHEDULER_IDLE_BEFORE_CLOSE', 0),
            'serializer': settings.get('SCHEDULER_SERIALIZER', None),
            'num_crawl_threads': settings.get('NUM_CRAWL_THREADS', 10),
            'blacklist': settings.get('BLACKLIST', r''),
            'whitelist': settings.get('WHITELIST', r'.*')
        }

        # Support serializer as a path to a module.
        if isinstance(kwargs.get('serializer'), six.string_types):
            kwargs['serializer'] = importlib.import_module(kwargs['serializer'])

        server = connection.from_settings(settings)
        # Ensure the connection is working.
        server.ping()

        return cls(server=server, **kwargs)

    def crawl_single(self, _):
        """
        通过url爬取网页，获取title和content
        """
        while True:
            url = self.dequeue('in')
            if url:
                self.logger.info(f"crawl:{url}")
                try:
                    r = requests.get(url, timeout=10)
                    if r.ok:
                        tree = fromstring(r.content)
                        title = tree.findtext('.//title')
                        if not self.blacklist.search(title) and self.whitelist.search(title):
                            result = {'url': url, 'title': title}
                            self.logger.info(f"produce:{url}")
                            self.enqueue(result)
                        else:
                            self.logger.info(f"filter:{url}")
                    else:
                        self.logger.info(f"discard:{url}")
                except Exception as e:
                    self.logger.info(f"discard:{url}")

    def crawl_bulk(self, n=0):
        n = self.num_crawl_threads if not n else n
        with ThreadPoolExecutor(n) as pool:
            pool.map(self.crawl_single, range(n))

def main(settings):
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    c = Crawler.from_settings(settings)
    c.open()
    #  c.crawl_single(1)
    c.crawl_bulk()
    c.close()

if __name__ == "__main__":
    from multiprocessing import Process
    settings = {'REDIS_HOST': '127.0.0.1',
                'REDIS_PORT': 6379,
                'SCHEDULER_SERIALIZER': 'json',
                'SCHEDULER_QUEUE_IN_KEY': 'digholes:queue_url_pool',
                'SCHEDULER_QUEUE_IN_CLASS': 'redisqueue.rqueues.LifoQueue',
                'SCHEDULER_QUEUE_OUT_KEY' : 'digholes:queue_response_pool'
                }
    p = Process(target=main, args=(settings,))
    p.start()
    p.join()
