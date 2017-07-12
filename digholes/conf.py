#  redis服务器信息
REDIS_HOST = '121.10.40.154'
REDIS_PORT = 6888

#  序列化格式
SCHEDULER_SERIALIZER = 'json'

#  监控输入文档的文件夹路径
INPUT_PATH = 'input'

#  以输入IP地址的多少子网掩码地址段来加入队列，即，是否取C段IP
SUBNET_MASK = 32

#  网页爬取时针对网页标题的黑名单
BLACKLIST = r'^(Apache Tomcat|Welcome to nginx|IIS7|Powered by lighttpd|Welcome to tengine!).*'

#  各组件线程数
#  同时扫描多少个IP
NUM_SCAN_HOST_PROCESSES = 1
#  扫描单个IP时同时扫描多少个端口
NUM_SCAN_PORT_THREADS = 777
#  注意，Linux系统默认限制了单个程序可同时打开的文件句柄为1024，可使用ulimit -n查看
#  需要保证 NUM_SCAN_HOST_PROCESSES * NUM_SCAN_PORT_THREADS < 最大文件句柄数，否则会导致同时打开文件句柄数过大而异常
#  Linux可以通过ulimit -n 10240指令来调大该参数
#  同时爬取多少张网页的内容
NUM_CRAWL_THREADS = 20

#  预处理程序在Redis上的KEY
SCHEDULER_DUPEFILTER_KEY_PRE = 'digholes:dupefilter'
SCHEDULER_QUEUE_KEY_PRE = 'digholes:queue_ip_pool'

#  端口扫描程序在Redis上的KEY
SCHEDULER_QUEUE_IN_KEY_SCAN = 'digholes:queue_ip_pool'
SCHEDULER_QUEUE_OUT_KEY_SCAN = 'digholes:queue_url_pool'

#  网页爬取程序在Redis上的KEY
SCHEDULER_QUEUE_IN_KEY_CRAWL = 'digholes:queue_url_pool'
SCHEDULER_QUEUE_OUT_KEY_CRAWL = 'digholes:queue_response_pool'
