import re
import time
import os
from urllib.parse import urlparse
import dns.resolver
import dns.rdtypes.IN.A
from IPy import IP
from itertools import chain
from concurrent.futures import ThreadPoolExecutor
from redisqueue.scheduler import DupeFilterScheduler
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

IPADDR_PATTERN = re.compile(r'^(?:\d+\.){3}\d+')
DOMAIN_PATTERN = re.compile(r'^(?:\w+\.){1,}\w+')


class Preprocessing(DupeFilterScheduler, FileSystemEventHandler):

    """
    用于对入库的数据进行预处理，包括格式检查、url的话进行dns解析、入库ip去重、默认自动入库ip所在的C段地址段
    """

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
            ips = (ip for ip_net in (IP(ip).make_net(24) for ip in resolve_result) for ip in ip_net)
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
                return (x for x in ip.make_net(24))

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
                    self.logger.info('输入文档格式错误')
        for ip in ips:
            self.enqueue(str(ip))

    def resolve_bulk(self, url_like_l, n=30):
        with ThreadPoolExecutor(n) as pool:
            pool.map(self.resolve_single, url_like_l)

    def on_created(self, event):
        try:
            with open(event.src_path) as f:
                data = f.readlines()
            self.resolve_bulk(data)
        except Exception as e:
            self.logger.info(e)

def main(settings):
    """测试代码
    :returns: TODO

    """
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
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

if __name__ == "__main__":
    from multiprocessing import Process
    settings = {'REDIS_HOST': '127.0.0.1',
                'REDIS_PORT': 6379,
                'SCHEDULER_SERIALIZER': 'json',
                'SCHEDULER_QUEUE_KEY': 'digholes:queue_ip_pool',
                'SCHEDULER_DUPEFILTER_KEY' : 'digholes:dupefilter',
                'INPUT_PATH': 'url',
                }
    p = Process(target=main, args=(settings,))
    p.start()
    p.join()