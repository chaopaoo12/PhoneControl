import os
import shutil
import time
from PhoneControl.BaseConsole.Phone import DnPlayer, BasiConsole

from datetime import datetime
import traceback
from functools import wraps

# 异常输出
def except_output(msg='异常'):
    # msg用于自定义函数的提示信息
    def except_execute(func):
        @wraps(func)
        def execept_print(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                sign = '=' * 60 + '\n'
                #print(f'{sign}>>>异常时间：\t{datetime.now()}\n>>>异常函数：\t{func.__name__}\n>>>{msg}：\t{e}')
                #print(f'{sign}{traceback.format_exc()}{sign}')
        return execept_print
    return except_execute

def retry(*args, **kwargs):
    def warpp(func):
        def inner():
            ret = func()
            max_retry = kwargs.get('max_retry')
            # 不传默认重试3次
            if not max_retry:
                max_retry = 3
            number = 0
            if not ret:
                while number < max_retry:
                    number += 1
                    print("尝试第:{}次".format(number))
                    result = func()
                    if result:
                        break
        return inner
    return warpp

class DnConsole(BasiConsole):
    # 请根据自己电脑配置

    #获取模拟器列表
    def get_list(self):
        cmd = os.popen(self.console + 'list2')
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(DnPlayer(dnplayer))
        return result

    #获取正在运行的模拟器列表
    def list_running(self) -> list:
        result = list()
        all = self.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result

    #检测指定序号的模拟器是否正在运行
    def is_running(self, index: int) -> bool:
        all = self.get_list()
        if index >= len(all):
            raise IndexError('%d is not exist' % index)
        return all[index].is_running()

    #执行shell命令
    def dnld(self, index: int, command: str, silence: bool = True):
        cmd = self.ld + '-s %d %s' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #执行adb命令,不建议使用,容易失控
    def adb(self, index: int, command: str, silence: bool = False) -> str:
        cmd = self.console + 'adb --index %d --command "%s"' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #安装apk 指定模拟器必须已经启动
    def install(self, index: int, path: str):
        shutil.copy(path, self.share_path + str(index) + '/update.apk')
        time.sleep(1)
        self.dnld(index, 'pm install /sdcard/Pictures/update.apk')

    #卸载apk 指定模拟器必须已经启动
    def uninstall(self, index: int, package: str):
        cmd = self.console + 'uninstallapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #启动App  指定模拟器必须已经启动
    def invokeapp(self, index: int, package: str):
        cmd = self.console + 'runapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #停止App  指定模拟器必须已经启动
    def stopapp(self, index: int, package: str):
        cmd = self.console + 'killapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #输入文字
    def input_text(self, index: int, text: str):
        cmd = self.console + 'action --index %d --key call.input --value %s' % (index, text)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #获取安装包列表
    def get_package_list(self, index: int) -> list:
        result = list()
        text = self.dnld(index, 'pm list packages')
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result

    #检测是否安装指定的应用
    def has_install(self, index: int, package: str):
        if self.is_running(index) is False:
            return False
        return package in self.get_package_list(index)

    #启动模拟器
    def launch(self, index: int):
        cmd = self.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #关闭模拟器
    def quit(self, index: int):
        cmd = self.console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置屏幕分辨率为1080×1920 下次启动时生效
    def set_screen_size(self, index: int):
        cmd = self.console + 'modify --index %d --resolution 1080,1920,480' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #点击或者长按某点
    def touch(self, index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            self.dnld(index, 'input tap %d %d' % (x, y))
        else:
            self.dnld(index, 'input touch %d %d %d' % (x, y, delay))

    #滑动
    def swipe(self, index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            self.dnld(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            self.dnld(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))



