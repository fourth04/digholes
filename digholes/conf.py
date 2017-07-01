
#  redis服务器信息
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6888

#  序列化格式
SCHEDULER_SERIALIZER = 'json'

#  监控输入文档的文件夹路径
INPUT_PATH = 'input'

#  以输入IP地址的多少子网掩码地址段来加入队列，即，是否取C段IP
SUBNET_MASK = 32

# 网页爬取时针对名称的黑名单
BLACKLIST = r'^Apache Tomcat.*|^Welcome to nginx.*'

# 各组件线程数
NUM_SCAN_THREAD = 5
NUM_CRAWLER_THREAD = 10
