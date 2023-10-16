import json
from urllib import parse
from urllib.parse import urlparse

import requests
import requests.utils
from bs4 import BeautifulSoup


class JDUser:
    def __init__(self, user):
        self.user = user
        self.api_url = 'https://api.m.jd.com/client.action'
        self.address = self.get_address()

    def get_sign(self, function_id, body):
        url = 'http://127.0.0.1:9998/sign'
        data = {
            'functionId': function_id,
            'body': body,
            'uuid': self.user.get('uuid'),
            'client': self.user.get('client'),
            'clientVersion': self.user.get('clientVersion'),
        }
        res = requests.post(url, data=json.dumps(data))
        return parse.parse_qs(res.text)

    def get_address(self):
        function_id = 'getAddressByPin'
        body = '{"isNeedPickAddressList":true,"isOneOrderMultipleAddress":false,"latitudeString":"wAgx7PWl/2s=","layerFlag":false,"longitudeString":"wAgx7PWl/2s=","pageId":0,"requestSourceType":2,"selectedPresentAddressId":0,"sourceType":2,"supportNewParamEncode":true}'
        sign = self.get_sign(function_id, body)
        params = {
            'functionId': function_id,
            'clientVersion': self.user.get('clientVersion'),
            'client': self.user.get('client'),
            'ef': self.user.get('params').get('ef'),
            'ep': self.user.get('params').get('ep'),
            'st': sign.get('st')[0],
            'sign': sign.get('sign')[0],
            'sv': sign.get('sv')[0],
        }
        headers = self.user.get('headers')
        data = {
            'body': body,
        }
        res = requests.post(self.api_url, params=params, headers=headers, cookies=self.user.get('cookies'),
                            data=data).json()
        return res.get('addressList')[0]

    def appoint(self, sku_id):
        function_id = 'appoint'
        body = '{"autoAddCart":"0","bsid":"","check":"0","ctext":"","isShowCode":"0","mad":"0","skuId":"' + sku_id + '","type":"4"}'
        sign = self.get_sign(function_id, body)
        params = {
            'functionId': function_id,
            'clientVersion': self.user.get('clientVersion'),
            'client': self.user.get('client'),
            'ef': self.user.get('params').get('ef'),
            'ep': self.user.get('params').get('ep'),
            'st': sign.get('st')[0],
            'sign': sign.get('sign')[0],
            'sv': sign.get('sv')[0],
        }
        headers = self.user.get('headers')
        data = {
            'body': body,
        }

        res = requests.post(self.api_url, params=params, headers=headers, cookies=self.user.get('cookies'),
                            data=data).json()
        print(f'预约结果: {res.get("title")} {self.user.get("name")}')

    def secskill(self, sku_id):
        session = requests.session()
        # 先获取genToken
        function_id = 'genToken'
        to = 'https://divide.jd.com/user_routing?skuId=' + sku_id + '&from=app'
        body = '{"action":"to","to":"' + to + '"}'
        sign = self.get_sign(function_id, body)
        params = {
            'functionId': function_id,
            'clientVersion': self.user.get('clientVersion'),
            'client': self.user.get('client'),
            'ef': self.user.get('params').get('ef'),
            'ep': self.user.get('params').get('ep'),
            'st': sign.get('st')[0],
            'sign': sign.get('sign')[0],
            'sv': sign.get('sv')[0],
        }
        data = {
            'body': body,
        }
        for name, value in self.user.get('cookies').items():
            session.cookies.set(name, value, path='/', domain='api.m.jd.com')
        res = session.post(self.api_url, params=params, headers=self.user.get('headers'), data=data,
                           allow_redirects=False)

        # 更新session的headers
        # session.headers.update(self.user.get('marathon headers'))
        # 跳转 https://un.m.jd.com/cgi-bin/app/appjmp
        gen_token = res.json()
        params = {
            'tokenKey': gen_token.get('tokenKey'),
            'to': to,
        }
        res = session.get(gen_token.get('url'), params=params, allow_redirects=False)
        # if res.status_code != 302:
        #     print(f'https://un.m.jd.com/cgi-bin/app/appjmp 返回不为302 {self.user.get("name")}')
        #     return
        # url_parsed = urlparse(res.headers.get('Location'))
        # re_url = url_parsed.scheme + '://' + url_parsed.netloc + url_parsed.path
        # if re_url != 'https://divide.jd.com/user_routing':
        #     print(
        #         f'跳转失败：企图 {re_url} 期望 https://divide.jd.com/user_routing {self.user.get("name")}')
        #     return
        #
        # # 跳转 https://divide.jd.com/user_routing
        # res = session.get(res.headers.get('Location'), allow_redirects=False)
        # if res.status_code != 302:
        #     print(f'https://divide.jd.com/user_routing 返回不为302 {self.user.get("name")}')
        #     return
        # url_parsed = urlparse(res.headers.get('Location'))
        # re_url = url_parsed.scheme + '://' + url_parsed.netloc + url_parsed.path
        # if re_url != 'https://marathon.jd.com/m/captcha.html':
        #     print(f'跳转失败：企图 {re_url} 期望 https://marathon.jd.com/m/captcha.html {self.user.get("name")}')
        #     return
        #
        # # 跳转 https://marathon.jd.com/m/captcha.html
        # res = session.get(res.headers.get('Location'), allow_redirects=False)
        # if res.status_code != 302:
        #     print(f'https://marathon.jd.com/m/captcha.html 返回不为302 {self.user.get("name")}')
        #     return
        # url_parsed = urlparse(res.headers.get('Location'))
        # re_url = url_parsed.scheme + '://' + url_parsed.netloc + url_parsed.path
        # if re_url != 'https://marathon.jd.com/seckillM/seckill.action':
        #     print(
        #         f'跳转失败：企图 {re_url} 期望 https://marathon.jd.com/seckillM/seckill.action {self.user.get("name")}')
        #     return
        #
        # # 跳转 https://marathon.jd.com/seckillM/seckill.action
        # res = session.get(res.headers.get('Location'), allow_redirects=False)
        # if res.status_code != 200:
        #     print(f'https://marathon.jd.com/seckillM/seckill.action 返回不为200 {self.user.get("name")}')
        #     return
        #
        # 访问 https://marathon.jd.com/seckillnew/orderService/init.action
        url = 'https://marathon.jd.com/seckillnew/orderService/init.action'
        data = {
            'sku': sku_id,
            'num': 1,
            'deliveryType': '',
            'id': self.address.get('Id'),
            'provinceId': self.address.get('IdProvince'),
            'cityId': self.address.get('IdCity'),
            'countyId': self.address.get('IdArea'),
            'townId': self.address.get('IdTown'),
        }
        res = session.post(url, data=data)
        if res.status_code != 200:
            print(f'https://marathon.jd.com/seckillnew/orderService/init.action 返回不为200 {self.user.get("name")}')
            return
        if res.json() is None:
            print(f'https://marathon.jd.com/seckillnew/orderService/init.action 返回为null {self.user.get("name")}')
            return

        # 提交订单
        order_info = res.json()
        url = 'https://marathon.jd.com/seckillnew/orderService/submitOrder.action'
        params = {
            'skuId': sku_id,
        }
        data = {
            'num': 1,
            'addressId': order_info.get('address').get('id'),
            'name': order_info.get('address').get('name'),
            'provinceId': order_info.get('address').get('provinceId'),
            'provinceName': order_info.get('address').get('provinceName'),
            'cityId': order_info.get('address').get('cityId'),
            'cityName': order_info.get('address').get('cityName'),
            'countyId': order_info.get('address').get('countyId'),
            'countyName': order_info.get('address').get('countyName'),
            'townId': order_info.get('address').get('townId'),
            'townName': order_info.get('address').get('townName'),
            'addressDetail': order_info.get('address').get('addressDetail'),
            'mobile': order_info.get('address').get('mobile'),
            'mobileKey': order_info.get('address').get('mobileKey'),
            'email': order_info.get('address').get('email'),
            'invoiceTitle': order_info.get('invoiceInfo').get('invoiceTitle'),
            'invoiceContent': order_info.get('invoiceInfo').get('invoiceContentType'),
            'invoicePhone': order_info.get('invoiceInfo').get('invoicePhone'),
            'invoicePhoneKey': order_info.get('invoiceInfo').get('invoicePhoneKey'),
            'invoice': True,
            'password': '',
            'codTimeType': 3,
            'paymentType': 4,
            'overseas': order_info.get('address').get('overseas'),
            'phone': order_info.get('address').get('phone'),
            'areaCode': order_info.get('address').get('areaCode'),
            'token': order_info.get('token'),
            'skuId': sku_id,
            # 'eid': self.user.get('marathon cookies').get('3AB9D23F7A4B3CSS'),
        }
        res = session.post(url, params=params, data=data)
        if res.status_code != 200:
            print(
                f'https://marathon.jd.com/seckillnew/orderService/submitOrder.action 返回不为200 {self.user.get("name")}')
            return
        try:
            res_json = res.json()
            print(f'{res_json} {self.user.get("name")}')
        except json.decoder.JSONDecodeError:
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            # title = soup.find('title')
            print(f'{title} {self.user.get("name")}')
