

from PhoneControl.shopping.jd import jd, sn


if __name__ == '__main__':
    jd = jd('127.0.0.1:62001')
    jd.get_app('https://item.m.jd.com/product/100012043978.html?ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=CopyURL')
    jd.reserve('10:00:00')
    jd.buy('12:00:00')