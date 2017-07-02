import sys
import getopt
import os
import json
import csv
from redisqueue.scheduler import Scheduler
import datetime
from utils import get_settings
import conf

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class GetResult(Scheduler):

    def get(self, number):
        result = [ self.dequeue() for _ in range(number) ]
        return [ _ for _ in result if _ ]

def main(settings):
    """测试代码
    :returns: TODO

    """
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

    try:
        # Short option syntax: "hv:"
        # Long option syntax: "help" or "verbose="
        opts, args = getopt.getopt(sys.argv[1:], "hv:n:o:", ["help", "verbose=", "number=", "output="])

    except getopt.GetoptError as err:
        # Print debug info
        logger.error(err)

    for option, argument in opts:
        if option in ("-h", "--help"):
            msg = '''
            Usage: python getresult.py [-n 100] [-o output.txt] [-h] [-v h]
            '''
            logger.info(msg)
        elif option in ("-v", "--verbose"):
            verbose = argument
            logger.info(verbose)
        elif option in ("-n", "--number"):
            number = int(argument)
        elif option in ("-o", "--output"):
            output = argument
            #  output = 'foo.json'
            #  output = 'foo.csv'
            #  output = 'foo.txt'
            suffix = os.path.basename(output).split('.')[-1]

    number = 100 if 'number' not in dir() else number
    output = "output_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".csv" if 'output' not in dir() else output

    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    g = GetResult.from_settings(settings)
    g.open()
    result = g.get(number)
    #  result = [
        #  {'url': 'www.baidu.com', 'title': 'baidu'},
        #  {'url': 'www.qq.com', 'title': 'qq'}
    #  ]
    g.close()
    if result:
        with open(output, 'w', newline='') as f:
            if suffix == 'csv':
                headers = result[0].keys()
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(result)
            elif suffix == 'json':
                json.dump(result, f)
            else:
                f.write(','.join(result[0].keys())+'\n')
                f.writelines(( ','.join(_.values())+'\n' for _ in result ))
        logger.info(f'保存{output}')

if __name__ == "__main__":
    #  settings = {'REDIS_HOST': '127.0.0.1',
                #  'REDIS_PORT': 6379,
                #  'SCHEDULER_SERIALIZER': 'json',
                #  }
    settings = get_settings(conf)
    settings_get = dict(
        SCHEDULER_QUEUE_KEY = 'digholes:queue_response_pool',
        **settings
    )
    main(settings_get)
