#导入bs4中的BeautifulSoup
from bs4 import BeautifulSoup
import os
from download import request

class mzitu():

    def save(self,img_url):
        # 这个函数保存图片
        name = img_url[-9:-4]
        print(u'开始保存：',img_url)
        img = request.get(img_url,3)
        f = open(name+".jpg",'ab')
        f.write(img.content)
        f.close()

    def img(self,page_url):
        # 这个函数处理图片页面地址获得图片的实际地址
        img_html = request.get(page_url,3)
        img_url = BeautifulSoup(img_html.text,'lxml').find('div',class_='main-image').find('img')['src']
        self.save(img_url)

    def html(self,href):
        # 这个函数是处理套图地址获得图片的页面地址
        html = request.get(href,3)
        # 查找所有的<span>标签获取第十个的<span>标签中的文本也就是最后一个页面了。
        html_Soup = BeautifulSoup(html.text, 'lxml')
        max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            # 调用img函数
            self.img(page_url)

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
        html = request.get(url,3)

        # 使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
        Soup = BeautifulSoup(html.text, 'lxml')

        # 使用BeautifulSoup解析网页过后就可以用找标签呐！（find_all是查找指定网页内的所有标签的意思，find_all返回的是一个列表。）
        # 意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
        all_a = Soup.find('div', class_='all').find_all('a')
        for a in all_a:
            # 取出a标签的文本
            title = a.get_text()
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
            # 调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！
            self.html(href)


#给函数all_url传入参数  你可以当作启动爬虫（就是入口）
Mzitu = mzitu()
Mzitu.all_url('http://www.mzitu.com/all')