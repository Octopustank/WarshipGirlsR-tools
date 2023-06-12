import  requests as rq
from bs4 import BeautifulSoup as bs
import json as js
import datetime as dt

URL = "https://www.zjsnrwiki.com/wiki/%E9%9F%B3%E4%B9%90%E9%89%B4%E8%B5%8F"
TIME_OUT = 8


def set_timeout(tm):
    global TIME_OUT
    TIME_OUT = tm

def get_music_html():##获取html字符串
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

def find_music_url(html):##解析html返回资源ulr列表
    soup = bs(html,"lxml")
    print("开始解析...")

    print("  find data-bind...",end="")
    temp = soup.find_all(attrs={"data-bind":True})
    print("  done")
    print("  detect urls...")

    urls = []
    count = 0
    for one in temp:
        one_js = js.loads(one.get("data-bind"))
        one_url = one_js['component']["params"]["playlist"][0]["navigationUrl"]
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
    file_name = "musicurls"+tm_nw+".txt"
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
    html = get_music_html()
    urls = find_music_url(html)
    return urls

if __name__ == "__main__":
    urls = main()
    output(urls)
