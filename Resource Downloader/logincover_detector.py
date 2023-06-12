import  requests as rq
from bs4 import BeautifulSoup as bs
import json as js
import datetime as dt

URL = "https://www.zjsnrwiki.com/wiki/%E5%8E%86%E4%BB%A3%E7%99%BB%E5%BD%95%E7%95%8C%E9%9D%A2"
TIME_OUT = 114


def set_timeout(tm):
    global TIME_OUT
    TIME_OUT = tm

def get_img_html():##获取html字符串
    print("连接网站...",end="")
    try:
        re = rq.get(URL,timeout=TIME_OUT)
        if re.status_code == 200:
            error = None
        else:
            error = re.status_code
##<确保访问
    except Exception as err:
        error = err
    print("done")
    if error is not None:
        print(f"  访问异常  Error:{error}\n")
        exit()
    else:
        print("  访问成功\n")
##确保访问>
    return re.text

def find_img_url(html):##解析html返回资源ulr列表
    soup = bs(html,"lxml")
    print("开始解析...")

    print("  find a(class=image)...",end="")
    temp = soup.find_all("a",class_="image")
    print("  done")
    print("  detect img and urls...")

    urls = []
    count = 0
    for one in temp:
        one_urls = one.find("img").attrs["srcset"]
        one_urls_list = one_urls.replace(" ","").split(",")
        one_url = one_urls_list[-1][:-2]
        count += 1
        print(f"\r    find {count} url(s)...",end="")
        urls.append(one_url)
    print("done")
    print("done\n")
    return urls

'''
def output(urls):##输出到文件
    print("输出到文件...",end="")
    tm_nw = dt.datetime.now().strftime('%Y%m%d')
    file_name = "logincoverurls"+tm_nw+".txt"
    with open(file_name,"w") as f:
        f.write("\n".join(urls))
    print(f'done (saved as "{file_name})"')
'''

def output(urls):
    tm_nw = dt.datetime.now().strftime('%Y%m%d')
    file_name = "musicurls"+tm_nw+".json"
    with open(file_name,"w") as f:
        js.dump(urls,f)

def main():##主程序
    html = get_img_html()
    urls = find_img_url(html)
    return urls

if __name__ == "__main__":
    urls = main()
    output(urls)
