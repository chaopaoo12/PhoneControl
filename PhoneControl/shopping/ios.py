import wda
import time
import datetime
from QUANTAXIS.QAUtil import QA_util_log_info
import traceback
from functools import wraps

def func_timer(function):
    '''
    用装饰器实现函数计时
    :param function: 需要计时的函数
    :return: None
    '''
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name = function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name = function.__name__,time = t1 - t0))
        return result
    return function_timer

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
                #print('{sign}>>>异常时间：\t{datetime.datetime.now()}\n>>>异常函数：\t{func.__name__}\n>>>{msg}：\t{e}')
                #print('{sign}{traceback.format_exc()}{sign}')
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

def time_check(start_time):

    d_tm = -0.1
    while d_tm <= 0:

        tm = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
        if tm > datetime.datetime.strptime(start_time, "%H:%M:%S"):
            seconds = (tm - datetime.datetime.strptime(start_time, "%H:%M:%S")).seconds
        else:
            seconds = (datetime.datetime.strptime(start_time, "%H:%M:%S") - tm).seconds* -1
        d_tm = seconds/60

        if d_tm <= -5:
            time.sleep(60)
        elif d_tm <= -1:
            time.sleep(10)
        else:
            pass

    print('time on {}'.format(start_time))

class phone():

    def __init__(self, port):
        self.phone = wda.Client('http://localhost:'+ port)
        self.package = None

    def open_url(self, url):
        if self.phone.app_current()['bundleId'] != 'com.apple.mobilesafari':
            self.phone.session("com.apple.mobilesafari")

        self.phone(label='地址').click()
        self.phone(label='地址').set_text(url)
        self.phone(label='前往').click()

    @except_output('异常信息')
    def get_app(self, url, package):
        self.package = package

        self.open_url(url)

        while package != self.phone.app_current()['bundleId']:
            if self.phone(label='立即打开').exists == False and self.phone(label='打开').exists == False:
                self.phone(label='刷新').click_exists()

            if self.phone(label='立即打开').click_exists():
                pass
            elif self.phone(label='打开').click_exists():
                pass

            self.phone(label='打开',visible=True).click_exists()

        if package == self.phone.app_current()['bundleId']:
            print('OK')
        else:
            print('ERROR')

    def start_app(self, package):
        self.package = package
        print('启动app: ' + package)
        self.phone.session(package)

    def reserve(self):
        QA_util_log_info('start reserve')

        print('JOB:未预约状态 开启预约程序')
        self.goto_reserve()

        print('预约成功 关闭应用')
        self.phone.app_terminate('com.android.browser')
        #预约完成退出程序
        self.phone.app_terminate(self.package)

    @except_output('异常信息a')
    def check_page(self):
        pass

    def buy(self, start_time):
        pass

    def goto_reserve(self):
        pass

    def cast_page(self):
        pass

    def goto_host(self):
        pass

    def goto_date(self):
        pass

    def goto_product(self):
        pass

    def goto_order(self, start_tm):
        pass

    def goto_payment(self):
        pass

    def deal_other(self):
        s_dict = {'host':1,
                  'date':2,
                  'product':3,
                  'order':4,
                  'payment':5,
                  'unknown':0,
                  }
        while s_dict[self.cast_page()] < 2:
            self.check_page()
            if self.cast_page() == 'host':
                self.goto_host()
                self.goto_date()


    def pre_order(self):
        start = datetime.datetime.now()
        self.check_page()
        self.goto_host(),
        self.goto_date(),
        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('pre_order cost {}'.format(dd))

    def order(self):
        page = self.cast_page()
        #if page == 'date':
        success=False
        print(page)

        while not success:
            self.check_page()
            start = datetime.datetime.now()
            while page != 'product' and page in ['host','date']:
                print('go to product')
                    #预订页 侦测
                self.goto_product()
                page = self.cast_page()
            end = datetime.datetime.now()
            dd = (end-start).seconds
            print('goto_product cost {}'.format(dd))

            start = datetime.datetime.now()
            while page == 'product':
                print('go to order')
                self.goto_order()
                page = self.cast_page()
            end = datetime.datetime.now()
            dd = (end-start).seconds
            print('goto_order cost {}'.format(dd))

            start = datetime.datetime.now()
            while page == 'order':
                print('go to payment')
                #确认订单
                self.goto_payment()
                page = self.cast_page()
                if page == 'payment':
                    success=True
                    break
            end = datetime.datetime.now()
            dd = (end-start).seconds
            print('goto_pay cost {}'.format(dd))

            self.deal_other()
            page = self.cast_page()
            print(page)

class jd(phone):

    def start_app(self, package='com.360buy.jdmobile'):
        self.package = package
        print('启动app')
        self.phone.session(self.package)
        while self.phone.app_current()['bundleId'] != self.package:
            time.sleep(1)

    @except_output('异常信息')
    def check_page(self):
        start = datetime.datetime.now()
        self.phone(label="忽略").click_exists()
        self.phone(label="msg windowclose").click_exists()
        self.phone(label="关闭页面").click_exists()

        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('checkpage cost {}'.format(dd))

    @func_timer
    def cast_page(self):
        if self.phone(label="京东收银台", className="XCUIElementTypeStaticText").exists:
            page = 'payment'
        elif self.phone(label="提交订单", className="XCUIElementTypeButton").exists:
            page = 'order'
        elif self.phone(label="分享", className="XCUIElementTypeButton").exists:
            page = 'product'
        elif self.phone(label="我的预约", className="XCUIElementTypeStaticText").exists:
            page = 'date'
        elif self.phone(label="设置", className="XCUIElementTypeButton").exists:
            page = 'host'
        else:
            page = 'unknown'
        return(page)

    @except_output('异常信息')
    def reserve_deal(self):
        self.phone(className="XCUIElementTypeButton", label="立即预约").click_exists()
        self.phone(className="XCUIElementTypeButton", label="增加购买数量").click_exists()
        self.phone(className="XCUIElementTypeButton", label="取消").click_exists()
        #self.phone(className="XCUIElementTypeButton", label="确定").click_exists()
        self.phone(className="XCUIElementTypeButton", label="知道啦").click_exists()

    @except_output('异常信息')
    def goto_reserve(self):
        self.check_page()
        start = datetime.datetime.now()
        while self.phone(label="已预约").exists == False:
            if self.phone(className="XCUIElementTypeButton", label="立即预约").exists:
                self.reserve_deal()
            if self.phone(label="等待预约").exists:
                print('等待预约')
            elif self.phone(label="等待抢购").exists:
                print('等待抢购')
                break
            else:
                self.reserve_deal()

        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('reserve cost {}'.format(dd))

    def reserve(self):
        QA_util_log_info('start reserve')
        self.check_page()

        print('JOB:未预约状态 开启预约程序')
        self.goto_reserve()

        print('预约成功 关闭应用')
        #预约完成退出程序
        self.phone.app_stop(self.package)

    @func_timer
    def goto_host(self):
        while self.phone(label="设置", className="XCUIElementTypeButton").exists == False:
            self.check_page()
            self.phone(className="XCUIElementTypeButton", text="我的").click_exists()

    @except_output('异常信息')
    @func_timer
    def goto_date(self):

        while self.phone(label="我的游戏与工具", className="XCUIElementTypeStaticText").exists == False:
            self.check_page()
            self.phone.swipe(0.773, 0.778, 0.25, 0.778, 0.5)
            time.sleep(1)
            self.phone.click(0.859, 0.778)
            time.sleep(1)

        while self.phone(name="我的预约", className="XCUIElementTypeNavigationBar").exists == False:
            if self.phone(className="XCUIElementTypeStaticText", label="我的预约").click_exists():
                pass
            elif self.phone(className="XCUIElementTypeStaticText", label="互动游戏").exists:
                self.phone.swipe_up()

        print('ready for the date page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))

    @except_output('异常信息')
    @func_timer
    def goto_product(self):
        while self.phone(label="分享", className="XCUIElementTypeButton").exists == False:

            if self.phone(label="预约抢购",className="XCUIElementTypeStaticText").exists:
                #self.phone(label="img 抢购中",className="XCUIElementTypeImage").click_exists()
                self.phone(label="茅台（MOUTAI）飞天 53%vol 500ml 贵州茅台酒（带杯）").click_exists()

            elif self.phone(label="我的预约", className="XCUIElementTypeStaticText").exists:
                print('界面崩坏 退回')
                self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
                self.phone(className="XCUIElementTypeStaticText", label="我的预约").click_exists()

        print('ready for the product page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))

    def total_buy(self, start_tm):
        print('step 1 for the product page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        k = 0
        n = 0
        mark = True
        time_check(start_tm)

        print('step 2 for the product page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        while mark and int(datetime.datetime.now().strftime("%H%M%S")) <= 121000:

            k += 1
            print('order strick {} at time {}'.format(k, datetime.datetime.now().strftime("%H:%M:%S")))
            self.phone.click(0.752, 0.966)
            time.sleep(0.3)
            self.phone.click(0.752, 0.966)
            #self.phone.screenshot().save("order-log-jd-{}-{}.jpg".format(k,datetime.datetime.now().strftime("%H%M%S")))
            if self.phone(name="立即抢购", className="XCUIElementTypeButton").click_exists():
                continue

            elif self.phone(label="抢购失败", className="XCUIElementTypeStaticText").exists:
                self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
                continue

            elif self.phone(name="返回重试", className="XCUIElementTypeButton").click_exists():
                continue

            elif self.phone(predicate='label="京东收银台"').exists:
                print('ready for the payment page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
                print('success!')
                mark = False
                self.phone.app_stop(self.package)

            #while self.phone(label="立即抢购", className="XCUIElementTypeButton").click_exists():
            #    k += 1
            #    print('order strick {} at time {}'.format(k, datetime.datetime.now().strftime("%H:%M:%S")))
            #    #self.phone(label="确定").click_exists()

            #while self.phone(name="返回重试", className="XCUIElementTypeButton").click_exists():
            #    pass

            ##self.phone.click(0.752, 0.966)

            #while self.phone(label="提交订单", className="XCUIElementTypeButton").click_exists():
            #    print('ready for the order page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
            #    n += 1
            #    print('payment strick {} at time {}'.format(n, datetime.datetime.now().strftime("%H:%M:%S")))

            #    if self.phone(label="提交订单", className="XCUIElementTypeButton").exists:
            #        self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
            #        break

            #    elif self.phone(predicate='label="京东收银台"').exists:
            #        print('ready for the payment page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
            #        print('success!')
            #        mark = False
            #        self.phone.app_stop(self.package)
            #        break
            #    else:
            #        self.phone.screenshot().save("payment-error-jd-{}-{}-{}.jpg".format(k,n,datetime.datetime.now().strftime("%H%M%S")))
            #        print('other error')

            #if self.phone(label="立即抢购", className="XCUIElementTypeButton").click_exists():
            #    self.phone(label="确定").click_exists()
            #    continue

            elif self.phone(label="提交订单", className="XCUIElementTypeButton").click_exists():
                self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
                continue

            elif self.phone(label="已预约", className="XCUIElementTypeStaticText").exists:
                pass

            elif self.phone(label="等待抢购", className="XCUIElementTypeStaticText").exists:
                pass

            elif self.phone(label="已抢完", className="XCUIElementTypeStaticText").exists:
                print('抢完了!')
                self.phone.screenshot().save("order-error-jd-{}-{}.jpg".format(k,datetime.datetime.now().strftime("%H%M%S")))
                mark = False
                self.phone.app_stop(self.package)

            else:
                self.phone.swipe_down()
                self.phone.screenshot().save("order-error-jd-{}-{}.jpg".format(k,datetime.datetime.now().strftime("%H%M%S")))

        print('已超时 {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        self.phone.app_stop(self.package)


    @except_output('异常信息')
    @func_timer
    def goto_order(self, start_tm):
        time_check(start_tm)
        k = 0
        while self.phone(predicate='label="提交订单"').exists == False:
            #self.phone(predicate='label="立即抢购"').click()
            #self.phone(predicate='label="确定"').click()
            if self.phone(label="立即抢购").click_exists():
                k += 1
                print('order strick {} at time {}'.format(k, datetime.datetime.now().strftime("%H:%M:%S")))
                if self.phone(label="抢购失败", className="XCUIElementTypeNavigationBar").exists:
                    self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
            self.phone(name="返回重试", className="XCUIElementTypeButton").click_exists()
            self.phone(label="确定").click_exists()

        print('ready for the order page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))

    @except_output('异常信息')
    @func_timer
    def goto_payment(self):
        k = 0
        #self.phone.click(0.752, 0.966)
        while self.phone(predicate='label="京东收银台"').exists == False:
            #self.phone.click(0.752, 0.966)
            if self.phone(label="提交订单").click_exists():
                k += 1
                print('payment strick {} at time {}'.format(k, datetime.datetime.now().strftime("%H:%M:%S")))

                if self.phone(label="提交订单", className="XCUIElementTypeButton").exists:
                    self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
                    self.goto_order()

            if self.phone(label="抢购失败", className="XCUIElementTypeNavigationBar").exists:
                self.phone(label="返回", className="XCUIElementTypeButton").click_exists()

        print('ready for the payment page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))

    def payment_deal(self):
        pass

    def buy(self, start_time):
        #判断是否找到预约按钮
        print('start buy')
        #提前三十秒激活
        self.check_page()
        self.pre_order()
        start = datetime.datetime.now()
        #time_check(start_time)
        self.order()
        print('抢购完成')
        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('total cost {}'.format(dd))

        self.phone.app_stop(self.package)


class sn(phone):

    def start_app(self, package='SuningEMall'):
        self.package = package
        print('启动app: '+ self.package)
        self.phone.app_start(self.package)
        while self.phone.app_current()['bundleId'] != self.package:
            time.sleep(1)

    @except_output('异常信息')
    def check_page(self):
        start = datetime.datetime.now()
        #要求分享地理位置系统级
        self.phone(label="SNSHPrecisonMarketClose").click_exists()
        self.phone(label="SNBS TestFlight Invitation Clo").click_exists()
        self.phone(label="snmember address voiceclose").click_exists()

        if self.phone(label="打开消息提醒，第一时间获取账户资产变动、物流消息").exists:
            self.phone.xpath('//Window[3]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Image[1]').click_exists()

        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('checkpage cost {}'.format(dd))

    def cast_page(self):
        if self.phone(label="订单中心", className="XCUIElementTypeStaticText").exists:
            page = 'payment'
        elif self.phone(label="提交订单", className="XCUIElementTypeButton").exists:
            page = 'order'
        elif self.phone(label="分享", className="XCUIElementTypeButton").exists:
            page = 'product'
        elif self.phone(label="更多", className="XCUIElementTypeButton").exists:
            page = 'date'
        elif self.phone(label="设置", className="XCUIElementTypeButton").exists:
            page = 'host'
        else:
            page = 'unknown'
        return(page)

    @except_output('异常信息')
    def reserve_deal(self):
        if self.phone(label="立即预约").exists:
            print('press:点击 立即预约 按钮')
            self.phone(label="立即预约").click()

        if self.phone(label="确定").exists:
            print('press:点击 确定 按钮')
            self.phone(label="确定").click()

        if self.phone(label="查看我的预约").exists:
            print('关闭预约成功通知')
            self.phone(label="查看我的预约").click()

    def goto_reserve(self):
        self.check_page()

        while self.phone(label="您已预约").exists == False and self.phone(label="等待抢购").exists == False:
            self.check_page()
            self.phone(label="立即预约").click_exists()
            self.phone(text="确定").click_exists()
            self.phone(label="查看我的预约！").click_exists()
            if self.phone(label="等待抢购").exists:
                print('等待抢购')
                break

    @except_output('异常信息')
    def goto_host(self):

        while self.phone(label="设置", className="XCUIElementTypeButton").exists == False:
            self.check_page()
            self.phone(label="我的").click_exists()
        time.sleep(3)
        self.phone.swipe_up()
        time.sleep(3)
        print('ready for the host page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))



    @except_output('异常信息')
    def goto_date(self):

        while self.phone(label="更多", className="XCUIElementTypeButton").exists == False:
            self.check_page()
            print(self.cast_page())
            if self.cast_page() not in ['host','date']:
                self.goto_host()
                self.phone.swipe_up()
                time.sleep(3)

            #self.phone(label="立即抢购", className="XCUIElementTypeButton").click_exists()
            if self.phone(label="我的预约", className="XCUIElementTypeButton").click_exists():
                pass
            elif self.phone(label="立即抢购", className="XCUIElementTypeButton").click_exists():
                pass
            #elif self.phone.xpath('//CollectionView/Cell[3]').click_exists():
            #    pass

            time.sleep(3)
        print('ready for the date page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))


    def goto_product(self):
        print('预约界面处理')
        while self.phone(label="分享", className="XCUIElementTypeButton").exists == False:
            self.phone(label="飞天53度 500mL 贵州茅台酒", className="XCUIElementTypeStaticText").click_exists()
        print('ready for the product page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))

    def total_buy(self, start_tm):
        print('step 1 for the product page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        k = 0
        n = 0
        mark =True
        time_check(start_tm)
        print('step 2 for the product page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        while mark and int(datetime.datetime.now().strftime("%H%M%S")) < 94000:#立即抢购

            k += 1
            print('order strick {} at time {}'.format(k, datetime.datetime.now().strftime("%H:%M:%S")))
            self.phone.click(0.752, 0.966)
            time.sleep(0.3)
            self.phone.click(0.752, 0.966)

            if self.phone(label="立即抢购", className="XCUIElementTypeButton").click_exists():
                #self.phone(label="确定").click_exists()
                continue

            elif self.phone(name="返回重试", className="XCUIElementTypeButton").click_exists():
                continue

            elif self.phone(label="提交订单", className="XCUIElementTypeButton").exists:
                self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
                continue

            elif self.phone(label="订单中心", className="XCUIElementTypeStaticText").exists:
                print('ready for the payment page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
                print('success!')
                mark = False
                self.phone.app_stop(self.package)
                break

            elif self.phone(label="抢购失败", className="XCUIElementTypeStaticText").exists:
                self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
                continue

            elif self.phone(label="您已预约", className="XCUIElementTypeStaticText").exists:
                pass

            elif self.phone(label="等待抢购", className="XCUIElementTypeStaticText").exists:
                pass

            elif self.phone(label="已抢完", className="XCUIElementTypeStaticText").exists:
                print('抢完了!')
                self.phone.screenshot().save("order-error-sn-{}-{}.jpg".format(k,datetime.datetime.now().strftime("%H%M%S")))
                mark = False
                self.phone.app_stop(self.package)

            else:
                self.phone.swipe_down()
                self.phone.screenshot().save("order-error-sn-{}-{}.jpg".format(k,datetime.datetime.now().strftime("%H%M%S")))

        print('已超时 {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        self.phone.app_stop(self.package)


    def goto_order(self, start_tm):
        time_check(start_tm)
        k = 0
        while self.phone(label="提交订单", className="XCUIElementTypeButton").exists == False:
            #self.phone(label="增加数量,购买数量1", className="XCUIElementTypeButton").exists:
            #self.phone.xpath('//ScrollView/Other[1]/Other[4]/Button[5]').click()
            #self.phone.click(0.752, 0.966)
            #self.phone.click(0.752, 0.966)
            if self.phone(label="立即抢购", className="XCUIElementTypeButton").click_exists():
                k += 1
                print('order strick {} at time {}'.format(k, datetime.datetime.now().strftime("%H:%M:%S")))
                if self.phone(label="抢购失败").exists:
                    self.phone(label="返回", className="XCUIElementTypeButton").click_exists()

            #self.phone(label="立即抢购").click_exists()
            self.phone(label="确定").click_exists()
            self.phone(label="知道了").click_exists()

            if self.phone(label="已抢完").exists:
                self.phone.app_stop(self.package)
                print('未抢到')

        print('ready for the order page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))

    def goto_payment(self):
        k = 0
        while self.phone(label="订单中心", className="XCUIElementTypeStaticText").exists == False:
            #self.phone.click(0.752, 0.966)
            if self.phone(label="提交订单").click_exists():
                k += 1
                print('payment strick {} at time {}'.format(k, datetime.datetime.now().strftime("%H:%M:%S")))
                if self.phone(label="提交订单", className="XCUIElementTypeButton").exists:
                    self.phone(label="返回", className="XCUIElementTypeButton").click_exists()
                    self.goto_order()
        print('ready for the payment page {}'.format(datetime.datetime.now().strftime("%H:%M:%S")))


    def buy(self, start_time):
        #判断是否找到预约按钮
        print('start buy')

        #提前三十秒激活

        self.check_page()
        self.pre_order()
        start = datetime.datetime.now()
        time_check(start_time)
        self.order()
        print('抢购完成')
        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('total cost {}'.format(dd))

        self.phone.app_stop(self.package)


