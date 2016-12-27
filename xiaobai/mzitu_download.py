#导入bs4中的BeautifulSoup
from bs4 import BeautifulSoup
import os
from download import down
from pymongo import MongoClient
import datetime
#from datetime import datetime

class mzitu():

    def __init__(self):
        # 与MongDB建立连接（这是默认连接本地MongDB数据库）
        client = MongoClient()
        # 选择一个数据库
        db = client['mzitudata']
        # 在meizixiezhenji这个数据库中，选择一个集合
        self.mzitu_collection = db['mzitu']
        # 用来保存页面主题
        self.title = ''
        # 用来保存页面地址
        self.url = ''
        # 初始化一个 列表 用来保存图片地址
        self.img_urls = []

    def save(self,img_url):
        # 这个函数保存图片
        name = img_url[-9:-4]
        print(u'开始保存：',img_url)
        img = down.get(img_url,3)
        f = open(name+".jpg",'ab')
        f.write(img.content)
        f.close()

    def img(self,page_url,max_span,page_num):#添加上面传递的参数
        # 这个函数处理图片页面地址获得图片的实际地址
        img_html = down.get(page_url,3)
        img_url = BeautifulSoup(img_html.text,'lxml').find('div',class_='main-image').find('img')['src']
        # 每一次 for page in range(1, int(max_span) + 1)获取到的图片地址都会添加到 img_urls这个初始化的列表
        self.img_urls.append(img_url)
        # 传递下来的两个参数用上了 当max_span和Page_num相等时，就是最后一张图片了，最后一次下载图片并保存到数据库中。
        if int(max_span) == page_num:
            self.save(img_url)
            # 这是构造一个字典，里面有啥都是中文，很好理解吧！
            post = {
                '标题':self.title,
                '主题页面':self.url,
                '图片地址':self.img_urls,
                '获取时间':datetime.datetime.now()
            }
            self.mzitu_collection.save(post)
        else:
            # max_span 不等于 page_num执行这下面
            self.save(img_url)

    def html(self,href):
        # 这个函数是处理套图地址获得图片的页面地址
        html = down.get(href,3)
        # 查找所有的<span>标签获取第十个的<span>标签中的文本也就是最后一个页面了。
        html_Soup = BeautifulSoup(html.text, 'lxml')
        max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        # 这个当作计数器用 （用来判断图片是否下载完毕）
        page_num = 0
        for page in range(1, int(max_span) + 1):
            # 每for循环一次就+1  （当page_num等于max_span的时候，就证明我们的在下载最后一张图片了）
            page_num = page_num + 1
            page_url = href + '/' + str(page)
            # 调用img函数,把上面我们我们需要的两个变量，传递给下一个函数。
            self.img(page_url,max_span,page_num)

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u'创建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("D:\mzitu", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def all_url(self,url):
        # 调用request函数把套图地址传进去会返回给我们一个response
        html = down.get(url,3)

        # 使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
        Soup = BeautifulSoup(html.text, 'lxml')

        # 使用BeautifulSoup解析网页过后就可以用找标签呐！（find_all是查找指定网页内的所有标签的意思，find_all返回的是一个列表。）
        # 意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
        all_a = Soup.find('div', class_='all').find_all('a')
        for a in all_a:
            # 取出a标签的文本
            title = a.get_text()
            # 将主题保存到self.title中
            self.title = title
            print(u'开始保存:',title)
            # 去掉空格
            #path = str(title).strip()
            # 我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            path = str(title).replace("?","_")
            #path = str(title)
            #path = re.sub('[\/:*?"<>|]', '-', path)

            # 调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            self.mkdir(path)

            # 切换到目录
            #os.chdir(path)
            os.chdir(os.path.join('D:\mzitu', path))

            href = a['href']
            # 将页面地址保存到self.url中
            self.url = href
            # 判断这个主题是否已经在数据库中、不在就运行else下的内容，在则忽略。
            if self.mzitu_collection.find_one({'主题页面':href}):
                print(u'这个页面已经爬取过了')
            else:
                # 调用html函数把href参数传递过去！href是套图的地址哦！
                self.html(href)


#给函数all_url传入参数  你可以当作启动爬虫（就是入口）
Mzitu = mzitu()
Mzitu.all_url('http://www.mzitu.com/all')