import requests
import json
from queue import Queue
import hashlib


queue = Queue()
email = "524135921@qq.com"
password = "qwe123!Q"

sha256 = hashlib.sha256()
sha256.update(password.encode("utf8"))
password = sha256.hexdigest()

host = "https://localhost:3443"

def setLogin():
    loginURL = "{0}/api/v1/me/login".format(host)
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    data = '{"email": "%s", "password": "%s", "remember_me": false}' % (email, password)
    try:
        res = requests.post(loginURL, data=data, headers=headers, verify=False)
        return res.headers["Set-Cookie"], res.headers["X-Auth"]
    except BaseException:
        print("setLogin error")

def newTarget(url):
    cookie, x = setLogin()
    reqURL = host + "/api/v1/targets"
    targetURL = url
    header = {
        'Content-Type': 'application/json;charset=utf-8',
        'X-Auth': x,
        'Cookie': cookie,
    }
    data = '{"description":"auto","address":"%s","criticality":"10"}' % targetURL
    try:
        res = requests.post(reqURL, data=data, headers=header, verify=False)
        return json.loads(res.content)["target_id"], cookie, x
    except BaseException:
        print("setTarget error")

def startScan(url):
    targetID, cookie, x = newTarget(url)
    scanURl = host + '/api/v1/scans'
    header = {
        'Content-Type': 'application/json;charset=utf-8',
        'X-Auth': x,
        'Cookie': cookie,
    }
    data = '{"target_id":"%s","profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"3d7b48c24a45f47a26f73630817693f8"}' % targetID
    try:
        res = requests.post(scanURl, data=data, headers=header, verify=False)
        print("====================================================")
        print(" start scan ")
        print("====================================================")
        print(res.content)
        print("====================================================")
        print(" finished")
        print("====================================================")
    except BaseException:
        print("startScan failed")

if __name__ == "__main__":
    with open("urlKR.txt",'r') as f :
        for line in f :
            if line.startswith("http://") or line.startswith("https://"):
                queue.put_nowait(line.replace('\n',''))
            else:
                queue.put_nowait("http://"+line.replace('\n',''))
            while 1:
                if not queue.empty():
                    startScan(queue.get())
                else:
                    break


import requests
import json
from queue import Queue
from gevent.pool import Pool
from gevent import monkey

monkey.patch_all()

queue = Queue()
email = "524135921@qq.com"
password = "qwe123!Q"

sha256 = hashlib.sha256()
sha256.update(password.encode("utf8"))
password = sha256.hexdigest()

host = "https://localhost:3443"

def setLogin () :
    loginURL = "{0}/api/v1/me/login" .format(host)
    header = {
        'Content-Type' : 'application/json;charset=utf-8'
    }
    data = '{"email": "%s", "password": "%s", "remember_me": false}' % (email, password)
    try :
        res = requests.post(loginURL, data=data, headers=header, verify= False )
        return res.headers[ "Set-Cookie" ], res.headers[ "X-Auth" ]
    except BaseException:
        print("setLogin error")

def newTarget (url) :
    cookie, x = setLogin()
    reqURL = host + "/api/v1/targets"
    targetURL = url
    header = {
        'Content-Type' : 'application/json;charset=utf-8' ,
        'X-Auth' : x,
        'Cookie' : cookie,
    }
    data = '{"description":"auto","address":"%s","criticality":"10"}' % targetURL
    try :
        res = requests.post(reqURL, data=data, headers=header, verify= False )
        return json.loads(res.content)[ "target_id" ], cookie, x
    except BaseException:
        print("setTarget error")

def startScan (url) :
    tarID, cookie, x = newTarget(url)
    scanURl = host + '/api/v1/scans'
    header = {
        'Content-Type' : 'application/json;charset=utf-8' ,
        'X-Auth' : x,
        'Cookie' : cookie,
    }
    data = '{"target_id":"%s","profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"3d7b48c24a45f47a26f73630817693f8"}' % targetID
        print("====================================================")
        print(" start scan ")
        print("====================================================")
        print(res.content)
        print("====================================================")
        print(" finished")
        print("====================================================")
    except BaseException:
        print("startScan failed")

def readFile () :
    with open( "hbcjw.txt" , 'r' ) as f:
        for line in f:
            if line.startswith( "http://" ) or line.startswith( "https://" ):
                queue.put_nowait(line.replace( '\n' , '' ))
            else :
                queue.put_nowait( "http://" + line.replace( '\n' , '' ))

def Run (n) :
    while True :
        if not queue.empty():
            startScan(queue.get())
        else :
            break

if __name__ == "__main__" :
    pool = Pool( 5 )
    readFile()
    pool.map(Run, xrange( 3 ))
