# Warship Girls R-tools
A tool set for Warship Girls R fans.  一些战舰少女R玩家的小工具

# Tool-1: Lock Screen Wallpaper Switcher 锁屏壁纸切换器
As we all know, the port in Warship Girls can change from day to night and from spring to autumn.   
众所周知，你游港区有昼夜季节变化。  
Therefore, we present to you a Python program that can switch the lock screen wallpaper on your Android phone based on this changing scenery!  
这就是一个小玩意让你安卓手机的锁屏界面同样如此！
### Features 功能
* It enables the automatic switching of your lock screen wallpaper based on season and time of day. 自动根据季节、天色换壁纸  
* It uses GPS to accurately calculate time periods. 使用定位来计算时间段  
* It runs on Termux, a terminal emulator application for Android OS extendible by variety of packages. 运行于Termux
##### #Attention 注意
Please note that in this program, we use the Chinese lunar calendar to calculate seasons, so if you are in the southern hemisphere, the seasons will be reversed.  使用农历，只适用于北半球
### Installation 安装
1. Install Termux <https://github.com/termux/termux-app> and Termux-api <https://github.com/termux/termux-api>. 安装Termux以及Termux-api  
2. Use the command `termux-setup-storage` to grant storage permissions. 获取存储权限  
3. Use the command `pkg upgrade` and `pkg install python, termux-api` to update and install packages. 安装包  
4. Use the command `pip install cnlunar, astral` to install packages. 安装库  
5. Use `cd ~/storage/shared` to access internal storage and find the program. 找到文件  
6. Use `python LSWS-WSGR.py` to run the program. 运行  
#if you want the program to run throughout the day, you can adjust Termux's power scheme to "allow background activity" in the phone settings and turn on "ACQUIRE WAKELOCK" in Termux. 如果要全天运行，请给Termux打开允许后台活动，并在通知栏Termux打开ACQUIRE WAKELOCK
### A problem 一个问题
If the program requests GPS but fails to get a response in time, it will get stuck until you type Ctrl+C to terminate it. Therefore, you may need to keep the GPS on your phone turned on. 如果没及时获取到定位，进程会被阻塞。
