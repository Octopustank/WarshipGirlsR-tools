import win32gui
import win32con
import win32api

def setWallpaper(imagepath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") 
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imagepath, 1+2)