import os
import cnlunar as cl
import datetime as dt
import json as js
from astral import LocationInfo, sun
import time as tm
import subprocess as sb


SEASON_DIC = {"春":"spring", "夏":"summer", "秋":"autumn", "冬":"winter"}
TIME_DIC = ["night", "dawn", "noon", "dusk", "night"]
JSON_PATH = os.getcwd()
PIC_PATH = "./portview"#输入港区图片路径


class Auto_screen_changer:
    def __init__(self):
        self.__dialog("init","开始初始化")

        self.season_dic = SEASON_DIC #季节中英文对应
        self.time_dic = TIME_DIC #一天中的时间段
        self.pic_path = PIC_PATH #图片路径
        self.json_path = JSON_PATH #数据存储位置
        self.data_file = os.path.join(self.json_path,"lks.json") #数据文件完整路径
        self.temp_file = os.path.join(self.json_path,"temp.json") #GPS定位反馈存储位置(临时文件)
        self.gps_wait = 5 #GPS请求等待时长


        self.get_time() #初始化当前时间self.now、self.today_ISO
        self.location = None #初始化地点 格式:[经度、纬度]
        self.season = None #初始化季节
        self.today_periods = None #初始化当日时间节点
        self.period_now = -1 #初始化当前处于的时间段序号

        self.__get_time_zone()#获取当前时区(datetime.deltatime)

        self.__check_datafile() #检查数据文件

        rd = self.__read_data()
        self.update_time = rd["time"] #读取/初始化慢更新数据的更新时间 格式:[year,week,weekday]
        self.location = rd["location"] #获取当前地点(经纬度)
        self.__dialog("read","读档读得",rd)

        self.__dialog("init","初始化完成","\n")


    def __gps(self): #对Termux进行GPS请求
        self.__dialog("GPS","发起请求")
        try:
            gps_response = js.loads(sb.run("termux-location -p gps", shell=True, timeout=self.gps_wait, stdout=sb.PIPE, stderr=sb.PIPE, check=True).stdout.decode())
            self.__dialog("GPS","请求成功")
            location = {"longitude":gps_response["longitude"], "latitude":gps_response["latitude"]} #截取经纬度数据
            return location
        except:
            self.__dialog("GPS","请求失败")
            return False


    def get_time(self): #获取当天时间数据
        self.now = dt.datetime.now() #时间
        self.today_ISO = list(dt.date.isocalendar(self.now)) #ISO[year,week,weekday]格式日期


    def __get_time_zone(self): #获取当前时区
        delt_utc = dt.datetime.now()-dt.datetime.utcnow()
        self.time_zone = dt.timezone(delt_utc)
        self.__dialog("timezone","时区:",self.time_zone)


    def __check_datafile(self): #检查数据文件(若不存在，则创建)
        if not os.path.exists(self.data_file):
            self.__save_data(None, True)

    def __save_data(self, data, creat = False): #保存数据文件
        if not creat: #不初始化数据文件,正常读取字典
            with open(self.data_file,"r") as f:
                dic = js.load(f)
        else: #初始化数据文件所用字典
            dic = {}

        dic["location"] = data
        dic["time"] = self.today_ISO

        with open(self.data_file,"w") as f:
            js.dump(dic,f) #写入文件


    def __read_data(self): #读取数据文件,返回字典
        with open(self.data_file,"r") as f:
            dic = js.load(f)
        return dic


    def __dialog(self, _class, words, data = None): #交互
        prt = f"[{_class}] {words}"
        if data is not None:
            prt = prt + f"\n  {data}"
        print(prt)


    def get_location(self): #获取当前位置
        self.__dialog("location","请求位置")
        
        location = self.location
        location =  self.__gps()

        if location: #如GPS请求成功
            self.location = location
            self.__dialog("location","位置获取成功",self.location)
            self.__save_data(self.location) #存储位置到数据文件

        else: #如未收到GPS请求的反馈
            self.__dialog("loaction","更新失败")
            if self.location: #如已经有位置数据
                self.__dialog("location","使用已有位置")

            else: #如没有现成位置数据
                data = self.__read_data()
                location = data["location"] #从数据文件中寻找可用的位置数据

                if location: #如数据文件中有可以位置数据
                    self.__dialog("location","读取存档位置",location)
                    self.location = location #采用该位置数据

                else: #数据文件没有位置数据
                    self.__dialog("location","无可用位置","退出程序")
                    tm.sleep(1);exit() #无法运行,直接终止程序


    def get_season(self): #计算季节

        today_lunar = cl.Lunar(self.now, godType='8char') #创建农历日期对象
        today_season = today_lunar.lunarSeason #获取季节
        self.season = self.season_dic[today_season[-1]] #转为所需格式
        self.__dialog("season","季节:",self.season)


    def get_periods(self): #获取当天时间节点
##        self.__dialog("time_period","计算时间段")
        location_dic = self.location

        location = LocationInfo('User', 'China', self.time_zone, location_dic["latitude"], location_dic["longitude"]) #创建地点对象
        s = sun.sun(location.observer, date = self.now, tzinfo = self.time_zone) #计算太阳时段

        tz_off = lambda x:x.replace(tzinfo = None)
        self.today_periods = list(map(tz_off, [s["dawn"], s["sunrise"], s["sunset"], s["dusk"]])) #获取所需数据并去除时区

        self.__dialog("time_period","时间节点:","\n  ".join(list(map(str,self.today_periods))))


    def cal_period(self): #定位时间段
##        self.__dialog("time_period","定位时间段")
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


    def update_location(self): #调用地点、季节、时间节点的全部获取(慢更新)
        self.get_location()
        self.update_time = self.today_ISO #跟进更新时间


    def change_screen(self): #调用Termux命令完成更改锁屏壁纸
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
        command = f"termux-wallpaper -f {file_path} -l"
        res = os.system(command) #调用命令

        self.__dialog("change_bg",res)


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
        self.get_time() #刷新程序时间

        if self.today_ISO != self.update_time or self.location is None:
            #若位置过期或缺失
            self.update_location()
            self.get_season()
            self.get_periods()
        elif self.season is None or self.today_periods is None:
            #若季节或时间段缺失
            self.get_season()
            self.get_periods()

        res = False
        res = self.cal_period()
        if res: #若时间段发生变化
            self.change_screen() #调用更改壁纸

        next_time = self.cal_delta_time() #获取下一次等待时长
        self.__dialog("main","完成一次运行",f"更改:{res}\n")
        return next_time + 1


if __name__ == "__main__":
    obj = Auto_screen_changer()
    while True:
        next_time = obj.run()
        tm.sleep(next_time)
