import os


class PhoneManage():

    def __init__(self, BasiConsole):
        self.console = BasiConsole.console
        self.ld = BasiConsole.ld
        self.share_path = BasiConsole.share_path

    #复制模拟器,被复制的模拟器不能启动
    def copy(self, name: str, index: int = 0):
        cmd = self.console + 'copy --name %s --from %d' % (name, index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #添加模拟器
    def add(self, name: str):
        cmd = self.console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #设置自动旋转
    def auto_rate(self, index: int, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = self.console + 'modify --index %d --autorotate %d' % (index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #改变设备信息 imei imsi simserial androidid mac值
    def change_device_data(self, index: int):
        # 改变设备信息
        cmd = self.console + 'modify --index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    #改变CPU数量
    def change_cpu_count(self, index: int, number: int):
        # 修改cpu数量
        cmd = self.console + 'modify --index %d --cpu %d' % (index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result