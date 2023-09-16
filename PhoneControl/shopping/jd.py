import uiautomator2 as u2
import time
import datetime
from QUANTAXIS.QAUtil import QA_util_log_info
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
                #print(f'{sign}>>>异常时间：\t{datetime.datetime.now()}\n>>>异常函数：\t{func.__name__}\n>>>{msg}：\t{e}')
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
            print(tm, d_tm)
        else:
            print(tm, d_tm)
            pass

    print('time on {}'.format(start_time))

class phone():

    def __init__(self, serialno):
        self.phone = u2.connect(serialno)
        self.phone.implicitly_wait(10)
        self.package = None

    @except_output('异常信息')
    def get_app(self, url, package):
        self.package = package

        self.phone.open_url(url)
        time.sleep(5)

        while self.phone(text='请选择要使用的应用').exists() == False:
            self.check_page()

            if self.phone(text='立即打开').exists():
                try:
                    print('click 京东APP')
                    self.phone(text='立即打开').click()
                except:
                    pass
            elif self.phone.xpath('//*[@resource-id="cartbuy"]/android.view.View[1]').exists:
                try:
                    self.phone.xpath('//*[@resource-id="cartbuy"]/android.view.View[1]').click()
                    print('click cartbuy')
                except:
                    pass

        #elif self.phone.xpath('//*[@resource-id="cartbuy"]/android.view.View[1]').exists:
        #    self.phone.xpath('//*[@resource-id="cartbuy"]/android.view.View[1]').click()
        while self.phone.app_current()['package'] != self.package:
            self.check_page()
            if self.phone(text='请选择要使用的应用').exists():
                print('alertTitle')
                if self.phone(resourceId='android.miui:id/app1').exists():
                    try:
                        self.phone(resourceId='android.miui:id/app1').click()
                        print('click app1')
                    except:
                        pass

    def start_app(self, package):
        self.package = package
        print('启动app: ' + package)
        self.phone.app_start(package)

    def reserve(self):
        QA_util_log_info('start reserve')

        print('JOB:未预约状态 开启预约程序')
        self.goto_reserve()

        print('预约成功 关闭应用')
        self.phone.app_clear('com.android.browser')
        self.phone.app_stop('com.android.browser')
        #预约完成退出程序
        self.phone.app_stop(self.package)

    @except_output('异常信息')
    def check_page(self):
        start = datetime.datetime.now()
        #要求分享地理位置系统级
        if self.phone(resourceId="com.android.browser:id/dont_share_button").exists():
            print('关闭系统地里位置共享提醒')
            self.phone(resourceId="com.android.browser:id/dont_share_button").click()

        #小米手机升级提醒
        if self.phone(text='发现新版本').exists():
            if self.phone(resourceId="android:id/button2").exists():
                print('关闭小米手机升级提醒')
                self.phone(resourceId="android:id/button2").click()

        #小米手机地理位置共享提醒
        if self.phone(resourceId='com.android.browser:id/ao4').exists():
            print('关闭小米手机地理位置共享提醒')
            self.phone(resourceId='com.android.browser:id/ao4').click()

        if self.phone(text='欢迎使用小米浏览器').exists():
            print('关闭小米手机浏览器提醒')
            self.phone(text='同意').click()

        if self.phone(text='打开').exists():
            print('关闭小米手机浏览器提醒')
            self.phone(text='打开').click()

        if self.phone(text='我知道了').exists():
            print('关闭小米手机系统提醒')
            self.phone(text='我知道了').click()

        #要求分享地理位置app级
        if self.phone(resourceId='com.jd.lib.productdetail.feature:id/jd_dialog_pos_button').exists():
            print('关闭京东APP地里位置共享提醒')
            self.phone(resourceId='com.jd.lib.productdetail.feature:id/jd_dialog_pos_button').click()

        if self.phone(resourceId='com.jingdong.app.mall:id/mj').exists():
            print('关闭京东APP新人礼包提醒')
            self.phone(resourceId='com.jingdong.app.mall:id/mj').click()

        if self.phone(resourceId="com.jingdong.app.mall:id/wp", text="发现新版本").exists():
            print('关闭京东APP升级提醒')
            if self.phone(resourceId="com.jingdong.app.mall:id/ws", text="取消").exists():
                self.phone(resourceId="com.jingdong.app.mall:id/ws", text="取消").click()

        #要求分享地理位置app级
        if self.phone(resourceId='com.suning.mobile.ebuy:id/update_cancel').exists():
            print('关闭苏宁APP升级提醒')
            self.phone(resourceId='com.suning.mobile.ebuy:id/update_cancel').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/btn_cdialog_left').exists():
            print('关闭苏宁全屏弹窗')
            self.phone(resourceId='com.suning.mobile.ebuy:id/btn_cdialog_left').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/cancel_img').exists():
            print('关闭苏宁图片全屏弹窗')
            self.phone(resourceId='com.suning.mobile.ebuy:id/cancel_img').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/close2').exists():
            print('关闭苏宁小弹窗')
            self.phone(resourceId='com.suning.mobile.ebuy:id/close2').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/tv_i_know').exists():
            print('关闭苏宁下单失败提醒')
            self.phone(resourceId='com.suning.mobile.ebuy:id/tv_i_know').click()

        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('checkpage cost {}'.format(dd))

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

    def goto_order(self):
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

            if self.cast_page() == 'host':
                self.goto_host()
                self.goto_date()
            else:
                self.phone.press('back')

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
            while page != 'product' and page in ['host','date']:
                print('go to product')
                if page in ['host','date']:
                    #预订页 侦测
                    self.goto_product()
                    mark = False
                else:
                    mark = True
                page = self.cast_page()
                if mark:
                    break

            while page == 'product':
                print('go to order')
                self.goto_order()
                page = self.cast_page()
                if page == 'order':
                    break
                elif page == 'date':
                    self.phone.press('back')
                else:
                    pass

            while page == 'order':
                print('go to payment')
                #确认订单
                self.goto_payment()
                page = self.cast_page()
                if page == 'payment':
                    success=True
                    break

            self.deal_other()
            page = self.cast_page()
            print(page)

class jd(phone):

    def start_app(self, package='com.jingdong.app.mall'):
        self.package = package
        print('启动app')
        self.phone.app_start(self.package)
        while self.phone.app_current()['package'] != self.package:
            time.sleep(1)

    @except_output('异常信息')
    def check_page(self):
        start = datetime.datetime.now()
        #要求分享地理位置系统级
        if self.phone(resourceId="com.android.browser:id/dont_share_button").exists():
            print('关闭系统地里位置共享提醒')
            self.phone(resourceId="com.android.browser:id/dont_share_button").click()

        #小米手机升级提醒
        if self.phone(text='发现新版本').exists():
            if self.phone(resourceId="android:id/button2").exists():
                print('关闭小米手机升级提醒')
                self.phone(resourceId="android:id/button2").click()

        #小米手机地理位置共享提醒
        if self.phone(resourceId='com.android.browser:id/ao4').exists():
            print('关闭小米手机地理位置共享提醒')
            self.phone(resourceId='com.android.browser:id/ao4').click()

        if self.phone(text='欢迎使用小米浏览器').exists():
            print('关闭小米手机浏览器提醒')
            self.phone(text='同意').click()

        if self.phone(text='打开').exists():
            print('关闭小米手机浏览器提醒')
            self.phone(text='打开').click()

        if self.phone(text='我知道了').exists():
            print('关闭小米手机系统提醒')
            self.phone(text='我知道了').click()

        #要求分享地理位置app级
        if self.phone(resourceId='com.jd.lib.productdetail.feature:id/jd_dialog_pos_button').exists():
            print('关闭京东APP地里位置共享提醒')
            self.phone(resourceId='com.jd.lib.productdetail.feature:id/jd_dialog_pos_button').click()

        if self.phone(resourceId='com.jingdong.app.mall:id/mj').exists():
            print('关闭京东APP新人礼包提醒')
            self.phone(resourceId='com.jingdong.app.mall:id/mj').click()

        if self.phone(resourceId="com.jingdong.app.mall:id/wp", text="发现新版本").exists():
            print('关闭京东APP升级提醒')
            if self.phone(resourceId="com.jingdong.app.mall:id/ws", text="取消").exists():
                self.phone(resourceId="com.jingdong.app.mall:id/ws", text="取消").click()

        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('checkpage cost {}'.format(dd))

    def cast_page(self):
        Activity = self.phone.app_current()['activity']
        if Activity == 'com.jd.lib.cashier.sdk.pay.view.CashierPayActivity':
            page = 'payment'
        #com.jd.lib.settlement.fillorder.activity.NewFillOrderActivity
        elif Activity == 'com.jd.lib.settlement.fillorder.activity.NewFillOrderActivity':
            page = 'order'
        elif Activity == 'com.jd.lib.productdetail.ProductDetailActivity':
            page = 'product'
        elif Activity == 'com.jingdong.app.mall.WebActivity':
            page = 'date'
        elif Activity == 'com.jingdong.app.mall.MainFrameActivity':
            page = 'host'
        else:
            page = 'unknown'
        return(page)

    #def cast_page(self):
    #    start = datetime.datetime.now()
    #    Activity = self.phone.app_current()['activity']

    #    #Activity = 'com.jd.lib.cashier.sdk.pay.view.CashierPayActivity'
    #    if Activity == 'com.jd.lib.cashier.sdk.pay.view.CashierPayActivity':
    #        page = 'payment'
    #    #com.jd.lib.settlement.fillorder.activity.NewFillOrderActivity
    #    elif Activity == 'com.jd.lib.settlement.fillorder.activity.NewFillOrderActivity':
    #        page = 'order'
    #    elif Activity == 'com.jd.lib.productdetail.ProductDetailActivity':
    #        #com.jd.lib.productdetail.ProductDetailActivity
    #        if self.phone(text="购物车").exists():
    #            page = 'productdetail'
    #        elif self.phone(text="确定").exists():
    #            page = 'productdetailmid'
    #        else:
    #            page = 'unknown'
    #    elif Activity == '.WebActivity':
    #        #.WebActivity
    #        if self.phone(resourceId="com.jingdong.app.mall:id/fd", text="我的预约").exists():
    #            page = 'date'
    #        else:
    #            page = 'unknown'
    #    elif Activity == '.MainFrameActivity':
    #        #.MainFrameActivity
    #        if self.phone(description="设置").exists() and self.phone(description="头像").exists():
    #            page = 'host'
    #        else:
    #            page = 'unknown'
    #    else:
    #        page = 'unknown'

    #    end = datetime.datetime.now()
    #    dd = (end-start).seconds
    #    print('cast_page cost {}'.format(dd))
    #    return(page)

    @except_output('异常信息')
    def reserve_deal(self):
        if self.phone(text="立即预约").exists():
            print('press:点击 立即预约 按钮')
            self.phone(text="立即预约").click()

        if self.phone(text="确定").exists():
            print('press:点击 确定 按钮')
            self.phone(text="确定").click()

        if self.phone(text="知道啦").exists():
            print('关闭预约成功通知')
            self.phone(text="知道啦").click()

    @except_output('异常信息')
    def goto_reserve(self):
        self.check_page()
        start = datetime.datetime.now()
        while self.phone(text="已预约").exists() == False:
            if self.phone(text="立即预约").exists():
                self.reserve_deal()
            elif self.phone(text="已预约").exists() and self.phone(description="分享").exists():
                print('已预约')
                break
            elif self.phone(text="等待预约").exists():
                print('等待预约')
            elif self.phone(text="知道啦").exists():
                self.reserve_deal()
            elif self.phone(text="购物车").exists() and self.phone(description="分享").exists():
                print('无需预约')
                break
            else:
                self.phone.press('back')

        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('reserve cost {}'.format(dd))

    def reserve(self):
        QA_util_log_info('start reserve')
        self.check_page()

        print('JOB:未预约状态 开启预约程序')
        self.goto_reserve()

        print('预约成功 关闭应用')
        self.phone.app_clear('com.android.browser')
        self.phone.app_stop('com.android.browser')
        #预约完成退出程序
        self.phone.app_stop(self.package)

    def goto_host(self):
        while self.cast_page() != 'host':
            self.check_page()
            self.phone.press('back')

        while self.phone(description="设置").exists() == False and self.phone(description="头像").exists() == False:
            self.check_page()
            if self.phone(resourceId="com.jingdong.app.mall:id/xk", text="我的").exists():
                self.phone(resourceId="com.jingdong.app.mall:id/xk", text="我的").click()

        try:
            self.phone.swipe_ext('up', 0.8)
            time.sleep(3)
        except:
            pass

    @except_output('异常信息')
    def goto_date(self):
        self.check_page()
        if self.cast_page() not in ['host','date']:
            self.goto_host()

        while self.phone(resourceId="com.jingdong.app.mall:id/fd", text="我的预约").exists() == False:
            self.check_page()
            if self.phone(text="我的预约").exists():
                self.phone(text="我的预约").click()
                time.sleep(5)
            else:
                print('host页面 下滑寻找我的预约')
                if self.phone(resourceId="com.jd.lib.personal.feature:id/mi", text="刷新中").exists():
                    time.sleep(3)
                else:
                    try:
                        self.phone.swipe_ext('up', 0.8)
                    except:
                        pass

    @except_output('异常信息')
    def goto_product(self):
        while self.phone(text="店铺").exists() == False:
            if self.phone(text="预约抢购").exists():
                if self.phone(text="飞天 53%vol 500ml 贵州茅台酒（带杯）").exists():
                    self.phone(text="飞天 53%vol 500ml 贵州茅台酒（带杯）").click()
            else:
                print('界面崩坏 退回')
                self.phone.press('back')
                self.goto_date()

    @except_output('异常信息')
    def goto_order(self):
        while self.cast_page() != 'order':
            if self.phone(resourceId="com.jd.lib.productdetail.feature:id/e", text = '立即抢购').exists():
                try:
                    self.phone(resourceId="com.jd.lib.productdetail.feature:id/e", text = '立即抢购').click()
                except:
                    pass

            if self.phone(description="返回").exists():
                try:
                    self.phone(description="返回").click()
                except:
                    pass

            if self.phone(text="确定").exists():
                try:
                    self.phone(text="确定").click()
                except:
                    pass

    @except_output('异常信息')
    def goto_payment(self):
        while self.cast_page() != 'payment':
            if self.phone(text="提交订单").exists():
                try:
                    self.phone(text="提交订单").click()
                except:
                    pass
                 #self.phone(resourceId="com.jingdong.app.mall:id/a93").exists()

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

    def start_app(self, package='com.suning.mobile.ebuy'):
        self.package = package
        print('启动app: '+ self.package)
        self.phone.app_start(self.package)
        while self.phone.app_current()['package'] != self.package:
            time.sleep(1)

    @except_output('异常信息')
    def check_page(self):
        start = datetime.datetime.now()
        #要求分享地理位置系统级
        if self.phone(resourceId="com.android.browser:id/dont_share_button").exists():
            print('关闭系统地里位置共享提醒')
            self.phone(resourceId="com.android.browser:id/dont_share_button").click()

        #小米手机升级提醒
        if self.phone(text='发现新版本').exists():
            if self.phone(resourceId="android:id/button2").exists():
                print('关闭小米手机升级提醒')
                self.phone(resourceId="android:id/button2").click()

        #小米手机地理位置共享提醒
        if self.phone(resourceId='com.android.browser:id/ao4').exists():
            print('关闭小米手机地理位置共享提醒')
            self.phone(resourceId='com.android.browser:id/ao4').click()

        if self.phone(text='欢迎使用小米浏览器').exists():
            print('关闭小米手机浏览器提醒')
            self.phone(text='同意').click()

        if self.phone(text='打开').exists():
            print('关闭小米手机浏览器提醒')
            self.phone(text='打开').click()

        if self.phone(text='我知道了').exists():
            print('关闭小米手机系统提醒')
            self.phone(text='我知道了').click()

        #要求分享地理位置app级
        if self.phone(resourceId='com.suning.mobile.ebuy:id/update_cancel').exists():
            print('关闭苏宁APP升级提醒')
            self.phone(resourceId='com.suning.mobile.ebuy:id/update_cancel').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/btn_cdialog_left').exists():
            print('关闭苏宁全屏弹窗')
            self.phone(resourceId='com.suning.mobile.ebuy:id/btn_cdialog_left').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/home_new_person_delete_iv').exists():
            print('关闭苏宁全屏弹窗')
            self.phone(resourceId='com.suning.mobile.ebuy:id/btn_cdialog_left').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/cancel_img').exists():
            print('关闭苏宁图片全屏弹窗')
            self.phone(resourceId='com.suning.mobile.ebuy:id/cancel_img').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/close2').exists():
            print('关闭苏宁小弹窗')
            self.phone(resourceId='com.suning.mobile.ebuy:id/close2').click()

        if self.phone(resourceId='com.suning.mobile.ebuy:id/tv_i_know').exists():
            print('关闭苏宁下单失败提醒')
            self.phone(resourceId='com.suning.mobile.ebuy:id/tv_i_know').click()

        end = datetime.datetime.now()
        dd = (end-start).seconds
        print('checkpage cost {}'.format(dd))

    def cast_page(self):
        'com.suning.mobile.yunxin.popup.PopOnlineBannerReminderActivity'

        Activity = self.phone.app_current()['activity']
        if Activity == 'com.suning.mobile.ebuy.transaction.newpay.ui.Cart3NewActivity':
            page = 'payment'
        elif Activity == 'com.suning.mobile.ebuy.transaction.shopcart2.ConfirmOrderInfoActivityNew':
            page = 'order'
        elif Activity == 'com.suning.mobile.ebuy.commodity.CommodityMainActivity':
            page = 'product'
        elif Activity == 'com.suning.mobile.ucwv.ui.WebViewActivity':
            page = 'date'
        elif Activity == 'com.suning.mobile.ebuy.host.MainActivity':
            page = 'host'
        else:
            page = 'unknown'
        return(page)

    #def cast_page(self):

    #    Activity = self.getActivity(self.package)
    #    if Activity == '.transaction.newpay.ui.Cart3NewActivity':
    #        page = 'payment'
    #    elif Activity == '.transaction.shopcart2.ConfirmOrderInfoActivityNew':
    #        page = 'order'
    #    elif Activity == '.commodity.CommodityMainActivity':
    #        #com.jd.lib.productdetail.ProductDetailActivity
    #        if self.phone(description="购物车").exists() and self.phone(description="店铺").exists():
    #            page = 'productdetail'
    #        elif self.phone(text="确定").exists():
    #            page = 'productdetailmid'
    #        else:
    #            page = 'unknown'
    #    elif Activity == 'com.suning.mobile.ucwv.ui.WebViewActivity':
    #        #.WebActivity
    #        if self.phone(resourceId="com.suning.mobile.ebuy:id/title", text="我的预约").exists():
    #            page = 'date'
    #        else:
    #            page = 'unknown'
    #    elif Activity == '.host.MainActivity':
    #        if self.phone(description="设置").exists() and self.phone(description="头像").exists():
    #            page = 'host'
    #        else:
    #            page = 'unknown'
    #    else:
    #        page = 'unknown'
    #    return(page)

    @except_output('异常信息')
    def reserve_deal(self):
        if self.phone(resourceId="com.suning.mobile.ebuy:id/btn_book_reservation").exists():
            print('press:点击 立即预约 按钮')
            self.phone(resourceId="com.suning.mobile.ebuy:id/btn_book_reservation").click()

        if self.phone(text="确定").exists():
            print('press:点击 确定 按钮')
            self.phone(text="确定").click()

        if self.phone(text="查看我的预约").exists():
            print('关闭预约成功通知')
            self.phone(text="查看我的预约").click()

    def goto_reserve(self):
        self.check_page()

        while self.phone(text="您已预约").exists() == False and self.phone(text="等待抢购").exists() == False:
            self.check_page()
            if self.phone(text="立即预约").exists() and self.phone(description="购物车").exists():
                self.reserve_deal()
            elif self.phone(text="您已预约").exists() and self.phone(description="购物车").exists():
                print('已预约')
                break
            elif self.phone(text="等待抢购").exists() and self.phone(description="分享").exists():
                print('已预约')
                break
            elif self.phone(text="等待预约").exists() and self.phone(description="购物车").exists():
                print('等待预约')
            elif self.phone(text="恭喜您预约成功！").exists():
                self.reserve_deal()
            elif self.phone(text="确定").exists():
                self.phone(text="确定").click()
            else:
                pass
                #self.phone.press('back')

    @except_output('异常信息')
    def goto_host(self):
        while self.cast_page() != 'host':
            self.check_page()
            self.phone.press('back')

        while self.phone(description="设置").exists() == False and self.phone(description="头像").exists() == False:
            self.check_page()
            if self.phone(description="我的").exists():
                self.phone(description="我的").click()

        try:
            self.phone.swipe_ext('up', 0.8)
            time.sleep(3)
        except:
            pass

    @except_output('异常信息')
    def goto_date(self):
        self.check_page()
        if self.cast_page() not in ['host','date']:
            self.goto_host()

        if self.phone(resourceId="立即抢购").exists():
            self.phone(text = '立即抢购').click()
        elif self.phone.xpath("""//*[@content-desc="我的预约"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]""").exists:
            self.phone.xpath("""//*[@content-desc="我的预约"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]""").click()
            time.sleep(5)
        #while self.phone(resourceId="com.suning.mobile.ebuy:id/title", text="我的预约").exists() == False:
        #    print(2)
        #    if self.phone.xpath("""//*[@content-desc="我的预约"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]""").exists:
        #        print(1)
        #        self.phone.xpath("""//*[@content-desc="我的预约"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]""").click()
        #    else:
        #        print('scroll')
        #        try:
        #            self.phone.swipe_ext('up', 0.8)
        #            time.sleep(3)
        #        except:
        #            pass

    def goto_product(self):
        print('预约界面处理')
        while self.phone(description="店铺").exists() == False:
            if self.phone(text="商品图片").exists():
                self.phone(text='商品图片').click()


    def goto_order(self):
        #if self.phone(description="增加数量").exists():

        if self.phone(resourceId="com.suning.mobile.ebuy:id/btn_goodsdetail_buy_now").exists():
            try:
                self.phone(resourceId="com.suning.mobile.ebuy:id/btn_goodsdetail_buy_now").click()
            except:
                pass

        if self.phone(text="知道了").exists():
            try:
                self.phone(text="知道了").click()
            except:
                pass

        if self.phone(text="确定").exists():
            try:
                self.phone(text="确定").click()
            except:
                pass

    def goto_payment(self):
        if self.phone(text="提交订单").exists():
            try:
                self.phone(text="提交订单").click()
            except:
                pass

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


