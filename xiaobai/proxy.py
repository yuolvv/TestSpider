import re
import requests

#初始化一个list用来存放我们获取到的IP
iplist = []
html = requests.get("http://haoip.cc/tiqu.htm")

#表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
iplistn = re.findall(r'r/>(.*?)<b',html.text,re.S)

for ip in iplistn:
    # re.sub 是re模块替换的方法，这儿表示将\n替换为空
    i = re.sub('\n','',ip)
    # 添加到我们上面初始化的list里面, i.strip()的意思是去掉字符串的空格哦！
    iplist.append(i.strip())
    print(i.strip())
print(iplist)