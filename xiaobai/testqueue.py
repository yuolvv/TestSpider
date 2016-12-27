from MongoQueue import MongoQueue
from bs4 import BeautifulSoup
from download import request

spider_queue = MongoQueue('testqueue','mziqueue')
def start(url):
    response = request.get(url,3)
    Soup = BeautifulSoup(response.text,'lxml')
    all_a = Soup.find('div',class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        url = a['href']
        """这个调用就是把URL写入MongoDB的队列了"""
        spider_queue.push(url,title)

if __name__ == "__main__":
    start('http://www.mzitu.com/all')





