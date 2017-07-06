import requests
import json
import hashlib
from functools import partial
import getopt
import sys

email = "524135921@qq.com"
raw_password = "qwe123!Q"

sha256 = hashlib.sha256()
sha256.update(raw_password.encode("utf8"))
password = sha256.hexdigest()

host = "https://localhost:3443"

def set_login():
    login_url = "{0}/api/v1/me/login".format(host)
    data = '{"email": "%s", "password": "%s", "remember_me": false}' % (email, password)
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    try:
        res = requests.post(login_url, data=data, headers=headers, verify=False)
        return res.headers["Set-Cookie"], res.headers["X-Auth"]
    except BaseException:
        print("set_login error")

def add_target(cookie, x, url):
    target_url = "{0}/api/v1/targets".format(host)
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'X-Auth': x,
        'Cookie': cookie,
    }
    data = '{"description":"auto","address":"%s","criticality":"10"}' % url
    try:
        res = requests.post(target_url, data=data, headers=headers, verify=False)
        return json.loads(res.content)["target_id"]
    except BaseException:
        print(f"setTarget error:{url}")

def start_scan(cookie, x, target_id):
    scan_url = '{0}/api/v1/scans'.format(host)
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'X-Auth': x,
        'Cookie': cookie,
    }
    data = '{"target_id":"%s","profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"3d7b48c24a45f47a26f73630817693f8"}' % target_id
    try:
        res = requests.post(scan_url, data=data, headers=headers, verify=False)
        return json.loads(res.content)["target_id"]
    except BaseException:
        print(f"start_scan failed:{target_id}")

def add_target_bulk(cookie, x, urls):
    p_add_target = partial(add_target, cookie, x)
    target_ids = map(p_add_target, urls)
    return [target_id for target_id in target_ids]

def start_scan_bulk(cookie, x, target_ids):
    p_start_scan = partial(start_scan, cookie, x)
    r_target_ids = map(p_start_scan, target_ids)
    return [target_id for target_id in r_target_ids]

def do_all_bulk(cookie, x, urls):
    target_ids = add_target_bulk(cookie, x, urls)
    r_target_ids = start_scan_bulk(cookie, x, target_ids)
    return [target_id for target_id in r_target_ids]

def read_file(filepath) :
    urls = [line.strip() if line.startswith( "http://" ) or line.startswith( "https://" ) else "http://"+line.strip() for line in open(filepath) if line.strip()]
    return urls

from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

def add_target_bulk_gvt(cookie, x, urls):
    p_add_target = partial(add_target, cookie, x)
    pool = Pool(5)
    target_ids = pool.map(p_add_target, urls)
    return [target_id for target_id in target_ids]

def start_scan_bulk_gvt(cookie, x, target_ids):
    p_start_scan = partial(start_scan, cookie, x)
    pool = Pool(5)
    r_target_ids = pool.map(p_start_scan, target_ids)
    return [target_id for target_id in r_target_ids]

def do_all_bulk_gvt(cookie, x, urls):
    target_ids = add_target_bulk(cookie, x, urls)
    r_target_ids = start_scan_bulk(cookie, x, target_ids)
    return [target_id for target_id in r_target_ids]

def main():
    try:
        # Short option syntax: "hv:"
        # Long option syntax: "help" or "verbose="
        opts, args = getopt.getopt(sys.argv[1:], "hv:i:t:", ["help", "verbose=", "input=", "task="])

    except getopt.GetoptError as err:
        # Print debug info
        print(str(err))

    for option, argument in opts:
        if option in ("-h", "--help"):
            print("使用格式为python awvs11.py -i urls.txt -t target/scan")
        elif option in ("-v", "--verbose"):
            verbose = argument
        elif option in ("-i", "--input"):
            input_filepath = argument
        elif option in ("-t", "--task"):
            task = argument
    operation = do_all_bulk_gvt if task == 'scan' else add_target_bulk_gvt

    urls = read_file(input_filepath)
    cookie, x = set_login()
    operation(cookie, x, urls)

if __name__ == "__main__" :
    main()
