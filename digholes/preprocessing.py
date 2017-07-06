import re
import os
from urllib.parse import urlparse
import dns.resolver
import dns.rdtypes.IN.A
from IPy import IP
from itertools import chain
from concurrent.futures import ThreadPoolExecutor
from redisqueue.scheduler import DupeFilterScheduler
import importlib
import six
import time
from redisqueue import connection
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

IPADDR_PATTERN = re.compile(r'^(?:\d+\.){3}\d+')
DOMAIN_PATTERN = re.compile(r'^(?:\w+\.){1,}\w+')


class Preprocessing(DupeFilterScheduler, FileSystemEventHandler):

    """
    用于对入库的数据进行预处理，包括格式检查、url的话进行dns解析、入库ip去重、默认自动入库ip所在的C段地址段
    """
    def __init__(self, server,
                 persist=False,
                 flush_on_start=False,
                 queue_key='queue:%(timestamp)s' % {'timestamp': int(time.time())},
                 queue_cls='redisqueue.rqueues.FifoQueue',
                 dupefilter_key='dupefilter:%(timestamp)s' % {'timestamp': int(time.time())},
                 dupefilter_cls='redisqueue.dupefilter.RFPDupeFilter',
                 dupefilter_debug=False,
                 idle_before_close=0,
                 serializer=None,
                 subnet_mask=32):
        """Initialize scheduler.

        Parameters
        ----------
        subnet_mask : int
            以当前ip地址的多少子网掩码地址段来加入队列，默认就是当前地址，不取C段
        """
        super().__init__(server, persist, flush_on_start, queue_key, queue_cls, dupefilter_key, dupefilter_cls, dupefilter_debug, idle_before_close, serializer)
        self.subnet_mask = subnet_mask

    @classmethod
    def from_settings(cls, settings):
        kwargs = {
            'persist': settings.get('SCHEDULER_PERSIST', True),
            'flush_on_start': settings.get('SCHEDULER_FLUSH_ON_START', False),
            'queue_key': settings.get('SCHEDULER_QUEUE_KEY', 'queue:%(timestamp)s' % {'timestamp': int(time.time())}),
            'queue_cls': settings.get('SCHEDULER_QUEUE_CLASS', 'redisqueue.rqueues.FifoQueue'),
            'dupefilter_key': settings.get('SCHEDULER_DUPEFILTER_KEY', 'dupefilter:%(timestamp)s' % {'timestamp': int(time.time())}),
            'dupefilter_cls': settings.get('SCHEDULER_DUPEFILTER_CLASS', 'redisqueue.dupefilter.RFPDupeFilter'),
            'dupefilter_debug': settings.get('SCHEDULER_DUPEFILTER_DEBUG', False),
            'idle_before_close': settings.get('SCHEDULER_IDLE_BEFORE_CLOSE', 0),
            'serializer': settings.get('SCHEDULER_SERIALIZER', None),
            'subnet_mask': settings.get('SUBNET_MASK', 32)
        }

        # Support serializer as a path to a module.
        if isinstance(kwargs.get('serializer'), six.string_types):
            kwargs['serializer'] = importlib.import_module(kwargs['serializer'])

        server = connection.from_settings(settings)
        # Ensure the connection is working.
        server.ping()

        return cls(server=server, **kwargs)

    def dns_resolve(self, domain):
        """将域名解析成地址段

        @param domain: 域名
        @type  domain: str

        @return: 地址段生成器
        @rtype : generator
        """
        try:
            a = dns.resolver.query(domain, 'A').response.answer
            #  即便是只查A记录，最后还是可能会出dns.rdtypes.ANY.CNAME.CNAME类型的记录，所以需要判断是否是dns.rdtypes.IN.A.A
            resolve_result = (j.address for i in a for j in i.items if isinstance(j, dns.rdtypes.IN.A.A))
            ips = (ip for ip_net in (IP(ip).make_net(self.subnet_mask) for ip in resolve_result) for ip in ip_net)
        except Exception:
            ips = []
        finally:
            return ips

    def ip_resolve(self, url_like):
        """解析IP地址字符串，
        - 如果是/32地址则将该地址字符串转换为所在C段所有地址
        - 如果是地址段，则返回该地址段所有地址
        - 其他格式则抛出异常

        @param url_like:  类似url格式的字符串
        @type  :  str

        @return:  地址段生成器
        @rtype :  generator

        @raise e:  地址格式错误
        """
        try:
            ip = IP(url_like)
        except ValueError as e:
            raise e
        else:
            if ip.len() > 1:
                return (x for x in ip)
            else:
                return (x for x in ip.make_net(self.subnet_mask))

    def resolve_single(self, url_like):
        parse_result = urlparse(url_like)
        hostname = parse_result.hostname
        if hostname:
            try:
                ips = self.ip_resolve(hostname)
            except ValueError:
                ips = self.dns_resolve(hostname)
        else:
            try:
                ips = self.ip_resolve(url_like)
            except ValueError:
                searched_ip = IPADDR_PATTERN.search(url_like)
                searched_domain = DOMAIN_PATTERN.search(url_like)
                if searched_ip:
                    ips = self.ip_resolve(searched_ip.group(0))
                elif searched_domain:
                    ips = self.dns_resolve(searched_domain.group(0))
                else:
                    ips = []
                    self.logger.info(f'{url_like}输入文档格式错误')
        for ip in ips:
            self.logger.info(f'produce:{ip}')
            self.enqueue(str(ip))

    def resolve_bulk(self, url_like_l, n=30):
        with ThreadPoolExecutor(n) as pool:
            pool.map(self.resolve_single, url_like_l)

    def on_created(self, event):
        try:
            self.logger.info(f"found file {event.src_path} created!")
            with open(event.src_path, encoding='utf8') as f:
                data = ( row.split(',')[0].strip() for row in f.readlines() if row.strip())
            self.resolve_bulk(data)
        except Exception as e:
            self.logger.info(e)

def main(settings):
    """测试代码
    :returns: TODO

    """
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    p = Preprocessing.from_settings(settings)
    p.open()
    path = os.path.abspath(settings.get('INPUT_PATH', '.'))
    if not os.path.exists(path):
        os.makedirs(path)
    p.logger.info(f"开始监控文件夹：{path}")
    observer = Observer()
    observer.schedule(p, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    p.close()

if __name__ == "__main__":
    settings = {'REDIS_HOST': '127.0.0.1',
                'REDIS_PORT': 6888,
                'SCHEDULER_SERIALIZER': 'json',
                'SCHEDULER_QUEUE_KEY': 'digholes:queue_ip_pool',
                'SCHEDULER_DUPEFILTER_KEY' : 'digholes:dupefilter',
                'INPUT_PATH': 'input',
                }
    #  from multiprocessing import Process
    #  p = Process(target=main, args=(settings,))
    #  p.start()
    #  p.join()
    main(settings)
