import os
import subprocess as sb
import sys
import json as js
import datetime as dt
import time as tm
import cnlunar as cl
from astral import LocationInfo, sun
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import win
import switcher as sw

SEASON_DIC = {"春":"spring", "夏":"summer", "秋":"autumn", "冬":"winter"}
TIME_DIC = ["night", "dawn", "noon", "dusk", "night"]
JSON_PATH = os.getcwd()
PIC_PATH = os.path.join(os.getcwd(),"portview")#输入图片路径
ICO_PATH = "E:\\Repositories\\Python\\WSGR_tools\\WallpaperSwitcher(forWindows)\\WallpaperSwitcher(forWindows)\\kun.ico"


class WallpaperSwitcher:
    def __init__(self, SEASON_DIC, TIME_DIC, JSON_PATH, PIC_PATH):
        self.__dialog("init","开始初始化")

        self.season_dic = SEASON_DIC #季节中英文对应
        self.time_dic = TIME_DIC #一天中的时间段
        self.pic_path = PIC_PATH #图片路径
        self.json_path = JSON_PATH #数据存储位置
        self.data_file = os.path.join(self.json_path,"data.json") #数据文件完整路径

        self.now = dt.datetime.now() #初始化当前时间
        self.location = None #初始化地点 格式:[经度、纬度]
        self.season = None #初始化季节
        self.today_periods = None #初始化当日时间节点
        self.period_now = -1 #初始化当前处于的时间段序号
        self.time_zone = None#初始化时区

        self.__check_datafile() #检查数据文件

        rd = self.__read_data()
        

        self.__dialog("init","初始化完成","\n")

    def __dialog(self, _class, words, data = None): #交互
        prt = f"[{_class}] {words}"
        if data is not None:
            prt = prt + f"\n  {data}"
        print(prt)

    def __check_datafile(self): #检查数据文件(若不存在，则创建)
        if not os.path.exists(self.data_file):
            self.save_data(None, None)

    def save_data(self, location, timezone): #保存数据文件
        dic = {}
        dic["location"] = location
        dic["timezone"] = timezone
        with open(self.data_file,"w") as f:
            js.dump(dic,f) #写入文件

    def __read_data(self): #读取数据文件,返回字典
        with open(self.data_file,"r") as f:
            dic = js.load(f)
        self.location = dic["location"] #获取当前地点(经纬度)
        self.timezone = dic["timezone"] #获取当前时区
        self.__dialog("read","读档读得",dic)

    def get_season(self): #计算季节
        today_lunar = cl.Lunar(self.now, godType='8char') #创建农历日期对象
        today_season = today_lunar.lunarSeason #获取季节
        self.season = self.season_dic[today_season[-1]] #转为所需格式
        self.__dialog("season","季节:",self.season)

    def get_periods(self): #获取当天时间节点
        location_dic = self.location

        location = LocationInfo('User', 'China', self.time_zone, location_dic["latitude"], location_dic["longitude"]) #创建地点对象
        s = sun.sun(location.observer, date = self.now, tzinfo = self.time_zone) #计算太阳时段

        tz_off = lambda x:x.replace(tzinfo = None)
        self.today_periods = list(map(tz_off, [s["dawn"], s["sunrise"], s["sunset"], s["dusk"]])) #获取所需数据并去除时区

        self.__dialog("time_period","时间节点:","\n  ".join(list(map(str,self.today_periods))))

    def cal_period(self): #定位时间段
        periods = self.today_periods
        nw = self.now

        nw_period = 0
        while  nw_period < len(periods) and nw > periods[nw_period]: #定位
            nw_period += 1

        self.__dialog("time_period","现在处于:", self.time_dic[nw_period])

        if nw_period != self.period_now: #若有变化
            self.period_now = nw_period #更新时间段定位
            return True
        else:
            return False

    def change_screen(self): #更改锁屏壁纸
        pic_path = self.pic_path
        season = self.season
        period_now = self.time_dic[self.period_now]

        dir_list = os.listdir(pic_path)
        for i in dir_list: #寻找所需壁纸文件
            if season in i:
                if period_now in i:
                    file = i
                    break
        file_path = os.path.join(pic_path, file)

        self.__dialog("change_bg","修改锁屏壁纸",file_path)
        sw.setWallpaper(file_path)

        self.__dialog("change_bg","done")


    def cal_delta_time(self): #计算距下一时间点的时长(s)
        today = self.now

        dt_max = dt.datetime.max
        today_end = today.replace(hour=dt_max.hour,minute=dt_max.minute,second=dt_max.second,microsecond=dt_max.microsecond)
        time_periods = self.today_periods + [today_end] #增加23:59:59:...的末节点

        next_period_start = time_periods[self.period_now] #计算时长
        delta_time = next_period_start - dt.datetime.now()
        next_time = delta_time.seconds
        self.__dialog("delta_time","下一时间节点(s):",next_time)
        return next_time

    def run(self): #运行时调用(快更新)
        self.__dialog("main","运行",dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.now = dt.datetime.now() #刷新程序时间
        print(self.location,self.timezone)
        if self.location is None or self.timezone is None:
            #若关键数据缺失
            win.edit_parameter(self.save_data, __file__)
            
        elif self.season is None or self.today_periods is None:
            #若季节或时间段缺失
            self.get_season()
            self.get_periods()

        res = self.cal_period()
        if res: #若时间段发生变化
            self.change_screen() #调用更改壁纸

        next_time = self.cal_delta_time() #获取下一次等待时长
        self.__dialog("main","完成一次运行",f"更改:{res}\n")
        return next_time + 1
    
    def on_saved(self):
        print("Parameters saved, continue running...")
        self.__read_data()
        
def edit_fun(location, timezone):
    task.save_data(location, timezone)


if __name__ == "__main__":
    task = WallpaperSwitcher(SEASON_DIC, TIME_DIC, JSON_PATH, PIC_PATH)
    while 1:
        temp = task.run()
        tm.sleep(temp)
