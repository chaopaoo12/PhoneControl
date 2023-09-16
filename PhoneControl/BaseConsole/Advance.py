import time
import cv2 as cv
from PhoneControl.BaseConsole.Basic import DnConsole
from PhoneControl.BaseConsole.Phone import UserInfo


class AdvanceConsole(DnConsole):

    def get_cur_activity_xml(self, index: int):
        # 获取当前activity的xml信息
        self.dnld(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(1)
        f = open(self.share_path + '/activity.xml' , 'r', encoding='utf-8')
        result = f.read()
        f.close()
        return result

    def get_user_info(self, index: int) -> UserInfo:
        xml = self.get_cur_activity_xml(index)
        usr = UserInfo(xml)
        if 'id' not in usr.info:
            return UserInfo()
        return usr

    #获取当前activity名称
    def get_activity_name(self, index: int):
        text = self.dnld(index, '"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    #等待某个activity出现
    def wait_activity(self, index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if self.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False

    #找图
    def find_pic(self, screen: str, template: str, threshold: float):
        try:
            scr = cv.imread(screen)
            tp = cv.imread(template)
            result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
        except cv.error:
            print('文件错误：', screen, template)
            time.sleep(1)
            try:
                scr = cv.imread(screen)
                tp = cv.imread(template)
                result = cv.matchTemplate(scr, tp, cv.TM_SQDIFF_NORMED)
            except cv.error:
                return False, None
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if min_val > threshold:
            print(template, min_val, max_val, min_loc, max_loc)
            return False, None
        print(template, min_val, min_loc)
        return True, min_loc

    #等待某个图片出现
    def wait_picture(self, index: int, timeout: int, template: str) -> bool:
        count = 0
        while count < timeout:
            self.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
            time.sleep(2)
            ret, loc = self.find_pic(self.share_path + '/apk_scr.png' , template, 0.001)
            if ret is False:
                print(loc)
                time.sleep(2)
                count += 2
                continue
            print(loc)
            return True
        return False

    # 在当前屏幕查看模板列表是否存在,是返回存在的模板,如果多个存在,返回找到的第一个模板
    def check_picture(self, index: int, templates: list):
        self.dnld(index, 'screencap -p /sdcard/Pictures/apk_scr.png')
        time.sleep(1)
        for i, t in enumerate(templates):
            ret, loc = self.find_pic(self.share_path + '/apk_scr.png' , t, 0.001)
            if ret is True:
                return i, loc
        return -1, None