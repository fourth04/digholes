import sys
import getopt
import os
import json
import csv
from redisqueue.scheduler import Scheduler
import datetime

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class GetResult(Scheduler):

    def get(self, number):
        result = [ self.dequeue() for _ in range(number) ]
        return [ _ for _ in result if _ ]

def main():
    """测试代码
    :returns: TODO

    """
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

    try:
        # Short option syntax: 'hv:'
        # Long option syntax: 'help' or 'verbose='
        opts, args = getopt.getopt(sys.argv[1:], 'hv:a:p:k:s:n:o:', ['help', 'verbose=', 'address=', 'port=', 'key', 'serializer', 'number=', 'output='])

    except getopt.GetoptError as err:
        # Print debug info
        logger.error(err)

    for option, argument in opts:
        if option in ('-h', '--help'):
            msg = '''
            Usage: python getresult.py [-h] [-v h] [-a 127.0.0.1] [-p 6379] [-k digholes:queue_response_pool] [-s json] [-n 100] [-o output.txt]
            '''
            logger.info(msg)
            return None
        elif option in ('-v', '--verbose'):
            verbose = argument
        elif option in ('-a', '--address'):
            address = argument
        elif option in ('-p', '--port'):
            port = int(argument)
        elif option in ('-s', '--serializer'):
            serializer = int(argument)
        elif option in ('-k', '--key'):
            key = argument
        elif option in ('-n', '--number'):
            number = int(argument)
        elif option in ('-o', '--output'):
            output = argument

    address = '127.0.0.1' if 'address' not in dir() else address
    port = 6379 if 'port' not in dir() else port
    key =  'digholes:queue_response_pool' if 'key' not in dir() else key
    serializer =  'json' if 'serializer' not in dir() else serializer
    number = 100 if 'number' not in dir() else number
    output = r'output/output_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv' if 'output' not in dir() else output
    dirname_output = os.path.dirname(output)
    if dirname_output and not os.path.exists(dirname_output):
        os.mkdir(dirname_output)
    suffix = os.path.basename(output).split('.')[-1]

    settings = {'REDIS_HOST': address,
                'REDIS_PORT': port,
                'SCHEDULER_QUEUE_KEY': key,
                'SCHEDULER_SERIALIZER': serializer,
                }
    g = GetResult.from_settings(settings)
    g.open()
    result = g.get(number)
    g.close()
    if result:
        with open(output, 'w', newline='', encoding='utf-8-sig') as f:
            if suffix == 'csv':
                headers = result[0].keys()
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                #  f_csv.writerows(result)
                for row in result:
                    try:
                        f_csv.writerow(row)
                    except Exception:
                        logger.warn(f'写入"{row}"时遇错，跳过此行')
            elif suffix == 'json':
                json.dump(result, f, ensure_ascii=False, indent=4)
            else:
                f.write(','.join(result[0].keys())+'\n')
                f.writelines(( ','.join(_.values())+'\n' for _ in result ))
        logger.info(f'保存至：{output}')

if __name__ == '__main__':
    main()
