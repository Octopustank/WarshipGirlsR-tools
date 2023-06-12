import requests as rq
import json as js
import os
from time import sleep
import datetime as dt

import logincover_detector as logincover
import music_detector as music
import portview_detector as portview


CHUNK = 8*1024*20 #20KB/0.2MB


PATH = os.getcwd()
TASKS = os.path.join(PATH,"tasks")
DOWNLOAD = os.path.join(PATH,"downloads")
if os.path.exists(TASKS) == False:
    os.mkdir(TASKS)
if os.path.exists(DOWNLOAD) == False:
    os.mkdir(DOWNLOAD)


def get_urls(target,wait_time):
    if "music" in target:
        music.set_timeout(wait_time)
        urls = music.main()
    elif "logincover" in target:
        logincover.set_timeout(wait_time)
        urls = logincover.main()
    elif "portview" in target:
        portview.set_timeout(wait_time)
        urls = portview.main()
    return urls

def creat_task(name, wait_time):
    lst = get_urls(name,wait_time)
    tm_nw = dt.datetime.now().strftime('%Y%m%d')
    data = {"name":name+tm_nw, "list":lst, "wait_time":wait_time}

    path = TASKS
    name = name+".json"

    with open(os.path.join(path,name),"w",encoding="utf-8") as f:
        js.dump(data,f)
    return name


def config():
    going = True
    print("*设置任务*")

    while going:
        wait_time = input(" 设置等待响应时长(s)[5]:")
        if wait_time=="":
            wait_time = 5
            break
        else:
            flag = True
            for i in wait_time:
                if not "0"<=i<="9":
                    flag = False
                    break
            if flag:
                wait_time = int(wait_time)
                break
        if wait_time=="exit":going=False;break
    print(f"等待时长设置为{wait_time}\n")
    if going:
        try:
            tm_nw = dt.datetime.now().strftime('#%Y%m%d#')
            print("创建音乐任务...")
            creat_task("music", wait_time)
            print("done\n----------")
            print("创建登录界面任务")
            creat_task("logincover", wait_time)
            print("done\n----------")
            print("创建港区景任务")
            creat_task("portview", wait_time)
            print("done\n")
        except Exception as err:
            print(f" ╳ 错误({err})")
    else:print("退出创建")


def show_tasks():
    path = TASKS
    lst = os.listdir(path)
    print(" No.  task文件  任务名 剩余下载数 ")
    print("----------------------------------")
    n = 0
    for one in lst:
        onepath = os.path.join(path,one)
        if os.path.isfile(onepath):
            try:
                with open(onepath,"r",encoding="utf-8") as f:
                    dic = js.load(f)
                    name = dic["name"]
                    num = len(dic["list"])
                n += 1
                print(f"{n}  {one}  {name}  {num}")
            except:
                continue
    return lst

def download_task(task):
    tk_path = os.path.join(TASKS,task)
    with open(tk_path,"r",encoding="utf-8") as f:
        dic = js.load(f)
    lst = dic["list"]
    timeout = dic["wait_time"]

    dw_path = os.path.join(DOWNLOAD,dic["name"])
    if os.path.exists(dw_path)==False:
        os.mkdir(dw_path)
    l = len(lst)
    n = 1
    errors = []
    while lst!=[]:
        print(f"*下载第{n}个(共{l}个)...")

        flag = True
        try:
            flag = download(lst[0],dw_path,timeout)
        except Exception as err:
            print(f" ╳ 调用下载错误 ({err})")
            flag = False

        if flag:
            lst.pop(0)
            n += 1
            update_tk(lst,tk_path)
        else:
            errors.append(lst.pop(0))
            n += 1
            update_tk(lst,tk_path)
        print()
    if errors!=[]:
        lst = errors
        print(" ╳ Warning:以下对象下载失败:\n{}".format('\n'.join(lst)))
        print("失败对象写回日志...",end="")
        update_tk(lst,tk_path)


def update_tk(temp,tk_path):
    with open(tk_path,"r",encoding="utf-8") as f:
         dic = js.load(f)
    dic["list"] = temp
    with open(tk_path,"w",encoding="utf-8") as f:
        js.dump(dic,f)
    print(f"已更新task文件({tk_path})")


def cal_bit(bit):
    size = bit/8
    tag = "B"
    if size>=1024:
        size = size/1024
        tag = "KB"
        if size>=1024:
            size = size/1024
            tag = "MB"
    return (size, tag)


def icon(full):
    if full is not None:
        full = int(full)
    icons = ['-','\\','|','/']
    chunk = CHUNK
    n = 0
    l = len(icons)
    size = 0
    while True:
        show = icons[n]+"下载中 "
        if full is not None:
            show = show+"{:.2%}".format(size/full)

        temp = cal_bit(size)
        show = show+" {:.2f}{}".format(temp[0],temp[1])

        if full is not None:
            temp = cal_bit(full)
            show = show+"/{:.2f}{}".format(temp[0],temp[1])
        yield show
        n = (n+1)%l
        size += CHUNK


def download(url,path,timeout):
    name = url.split("/")[-1]
    print(f"  下载文件:{name}")
    name = check_filename(path,name)
    print(f"     文件将保存至:{name}")

    try:
        rt = rq.get(url, stream=True, timeout=timeout)
    except Exception as err:
        print(f"  ╳ 访问URL失败 ({err})")
        return False

    try:
        length = rt.headers['Content-Length']
    except Exception as err:
        print(f"   warning:获取文件大小失败(err)")
        length = None
    chunk = CHUNK
    perform_icon = icon(length)
    ico_nw = ""
    try:
        with open(name,"wb") as f:
            for one in rt.iter_content(chunk_size=chunk):
                if one:
                    f.write(one)
                    ico_nw = next(perform_icon)
                    print("\r"+ico_nw,end="")
        print("\r  √ 下载成功"+" "*(len(ico_nw)-7))
        return True
    except Exception as err:
        print(f"  ╳ 下载失败 ({err})")
        return False

def check_filename(path,original_name):
    exist_names = os.listdir(path)
    first_name, last_name = os.path.splitext(original_name)
    name = [first_name, last_name, 0]

    make_name = lambda x:x[0]+ (str(x[2])if x[2]!=0 else "") +x[1]

    while True:
        if not make_name(name) in exist_names:
            break
        name[2]+=1
    name = make_name(name)
    return os.path.join(path,name)


def download_dialog():
    print("#下载任务#")
    lst = show_tasks()
    print("下载内容选择(输入No.):")
    flag = True
    while flag:
        com = input()
        if com.lower() in ["exit",""]:
            print("退出下载")
            break
        try:
            com = int(com)
            if 0 < com <= len(lst):
                download_task(lst[int(com)-1])
                flag = False
        except:pass
        if flag:print("再试一次")



if __name__=="__main__":
    HELP = "\
    • config   (cfg) : 设置任务\n\
    • showtask  (st) : 列出任务\n\
    • download  (dt) : 下载任务"
    print("批量下载器")
    while 1:
        command = input(">>>")
        if command.lower() in ["","exit"]:
            print("退出")
            sleep(1)
            exit()
        elif command.lower() in ["help","h"]:
            print("帮助:")
            print(HELP)
        elif command.lower() in ["config","cfg"]:
            config()
        elif command.lower() in ["showtask","st"]:
            show_tasks()
        elif command.lower() in ["download","dt"]:
            download_dialog()
    
