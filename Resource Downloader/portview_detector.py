import  requests as rq
from bs4 import BeautifulSoup as bs
import json as js
import datetime as dt

URL = "https://www.zjsnrwiki.com/wiki/%E6%B8%AF%E5%8F%A3"
WEBSITE= "https://www.zjsnrwiki.com"
TIME_OUT = 114


def set_timeout(tm):
    global TIME_OUT
##    TIME_OUT = tm
    print(" 港区景 访问等待时间:114s")

def get_img_html(url = URL, dialog = True):##获取html字符串
    if not dialog:
        print("\r"+" "*20,end="")
        print("\r连接网站...",end="")
    else:
        print("连接网站...",end="")

    try:
        re = rq.get(url,timeout=TIME_OUT)
        if re.status_code == 200:
            error = None
        else:
            error = re.status_code
##<确保访问
    except Exception as err:
        error = err
    if dialog:
        print("done")
##    else:
##        print("done",end="")
    if error is not None:
        if dialog:
            print(f"  访问异常  Error:{error}\n")
        else:
            print(f"    !访问异常(url:{url}) Error:{error}")
        exit()
    else:
        if dialog:
            print("  访问成功\n")
##        else:
##            print(" (访问成功)",end="")
##确保访问>
    return re.text

def find_img_url(html):##解析html返回资源ulr列表
    website = WEBSITE
    soup = bs(html,"lxml")
    print("开始解析...")

    print("  find a(class=image)...",end="")
    temp = soup.find_all("a",class_="image")
    print("  done")
    
    print("  detect&connect&get img_urls...")
    urls = []
    count = 0
    for one in temp:
        one_urls = one.attrs["href"]
        one_urls = website.strip('/') + "/" + one_urls.strip('/')
        one_view_html = get_img_html(url = one_urls, dialog = False)
        one_view_soup = bs(one_view_html,"lxml")
        one_temp = one_view_soup.find_all("a",class_="internal")[0]
        one_url = one_temp.attrs["href"]
        count += 1
        print("\r"+" "*20+f"find {count} img_view_url(s)...",end="")
        urls.append(one_url)
    print("done")

    return urls

'''
def output(urls):##输出到文件
    print("输出到文件...",end="")
    tm_nw = dt.datetime.now().strftime('%Y%m%d')
    file_name = "portview"+tm_nw+".txt"
    with open(file_name,"w") as f:
        f.write("\n".join(urls))
    print(f'done (saved as "{file_name})"')
'''

def output(urls):
    tm_nw = dt.datetime.now().strftime('%Y%m%d')
    file_name = "portview"+tm_nw+".json"
    with open(file_name,"w") as f:
        js.dump(urls,f)

def main():##主程序
    html = get_img_html()
    urls = find_img_url(html)
    return urls

if __name__ == "__main__":
    urls = main()
    output(urls)
