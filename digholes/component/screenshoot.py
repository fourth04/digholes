from concurrent.futures import ThreadPoolExecutor
import requests
import time
from threading import Timer
from selenium import webdriver
from urllib.parse import urlparse
import os
import logging
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def screenshoot(urls):
    """截图

    :url: TODO
    :returns: TODO

    """
    driver = webdriver.PhantomJS()
    for url in urls:
        logger.info(f'尝试访问:{url}')
        try:
            r = requests.get(url)
        except Exception as e:
            logger.error(f'无响应:{url}')
        else:
            logger.info(f'成功访问:{url}，解析网页内容')
            if r.ok:
                logger.info(f'电信网站:{url}，尝试截图')
                timer = Timer(15, driver.close)
                try:
                    timer.start()
                    driver.get(url)
                finally:
                    if timer.finished.is_set():
                        driver.start_session({'browser_name':'phantomjs'})
                    else:
                        timer.cancel()
                        driver.execute_script("""
                            (function () {
                                var y = 0;
                                var step = 100;
                                window.scroll(0, 0);

                                function f() {
                                    if (y < document.body.scrollHeight) {
                                        y += step;
                                        window.scroll(0, y);
                                        setTimeout(f, 100);
                                    } else {
                                        window.scroll(0, 0);
                                        document.title += "scroll-done";
                                    }
                                }

                                setTimeout(f, 1000);
                            })();
                        """)

                        for i in range(3):
                            if "scroll-done" in driver.title:
                                break
                            time.sleep(10)

                        dname = urlparse(url).netloc.replace(':', '：')
                        screenshoot_dir = 'ScreenShoot'
                        if not os.path.isdir(screenshoot_dir):
                            os.mkdir(screenshoot_dir)
                        file_path = os.path.join(screenshoot_dir, dname + '.png')
                        driver.save_screenshot(file_path)
            else:
                logger.error(f'响应异常:{url}')

if __name__ == "__main__":
    import math
    logging.basicConfig(level=logging.INFO)
    urls = [url.strip() for url in open('urls/scrapy_urls2.txt')]
    n = 20
    with ThreadPoolExecutor(n) as pool:
        pool.map(screenshoot, [urls[x:x+math.ceil(len(urls)/n)] for x in range(0, len(urls), math.ceil(len(urls)/n))])
