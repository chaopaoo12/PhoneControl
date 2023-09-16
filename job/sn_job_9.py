
from PhoneControl.shopping.jd import jd, sn


if __name__ == '__main__':
    sn = sn('127.0.0.1:62001')
    sn.get_app('https://m.suning.com/product/0000000000/000000011001203841.html?utm_campaign=1675259015181677697&utm_source=share-copyurl&utm_medium=2cd5ed46-copyurl')
    sn.reserve('08:30:00')
    sn.buy('09:30:00')


