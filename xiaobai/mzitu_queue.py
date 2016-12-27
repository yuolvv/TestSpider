#导入bs4中的BeautifulSoup
from bs4 import BeautifulSoup
import os
import time
import threading
import multiprocessing
from download import request
from MongoQueue import MongoQueue

SLEEP_TIME = 1

def mzitu_crawler(max_threads=10):
    # 这个是我们获取URL的队列
    crawl_queue = MongoQueue('mzituqueue','crawl_queue')

    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print('队列没有数据')
                break
            else:
                img_urls = []
                req = request.get(url,3).text
                title = crawl_queue.pop_title(url)
                mkdir(title)
                os.chdir('D:\mzitu\\'+title)
                max_span = BeautifulSoup(req.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1, int(max_span) + 1):
                    page_url = url + '/' + str(page)
                    img_url = BeautifulSoup(request.get(page_url,3).text,'lxml').find('div',class_='main-image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)
                # 设置为完成状态
                crawl_queue.complete(url)

    def save(img_url):
        # 这个函数保存图片
        name = img_url[-9:-4]
        print(u'开始保存：',img_url)
        img = request.get(img_url,3)
        f = open(name+".jpg",'ab')
        f.write(img.content)
        f.close()

    def mkdir(path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u'创建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("D:\mzitu", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    threads = []

    while threads or crawl_queue:
        """
        这儿crawl_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
        threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
        """
        for thread in threads:
            if not thread.is_alive():
                # is_alive是判断是否为空,不是空则在队列中删掉
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():
            # 线程池中的线程少于max_threads 或者 crawl_qeue时
            # 创建线程
            thread = threading.Thread(target=pageurl_crawler)
            # 设置守护线程
            thread.setDaemon(True)
            # 启动线程
            thread.start()
            # 添加进线程队列
            threads.append(thread)
        time.sleep(SLEEP_TIME)

def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为：',num_cpus)
    for i in range(num_cpus):
        #创建进程
        p = multiprocessing.Process(target=mzitu_crawler)
        #启动进程
        p.start()
        #添加进进程队列
        process.append(p)

    for p in process:
        #等待进程队列里面的进程结束
        p.join()

if __name__ == "__main__":
    process_crawler()