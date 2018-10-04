#coding=utf-8
import sys
sys.path.append(r'G:\gui_exchange\base')
from deploy import http_get_request,http_post_request,api_key_get,api_key_post
from config.find_config import ReadIni
import time
import datetime

class RunMethod(object):
    def __init__(self):
        pass

    # 币币账户
    def get_user_info(self):
        params={}
        url='/api/v1/userinfo.do'
        return api_key_post(params, url)


    def get_trade(self, symbol):
        params={'symbol':symbol}
        url='/api/v1/ticker.do'
        return api_key_get(params, url)


    def trade_display(slef, symbol, trade_dict):
        high=trade_dict['ticker']['high']
        low=trade_dict['ticker']['low']
        last=trade_dict['ticker']['last']
        print("%s交易对\n当前成交价:%s\n24小时最高价:%s\n24小时最低价%s\n"%(symbol, last, high, low))


    def kline(self, symbol, time, size):
        params={
                'symbol':symbol,
                'type':time,
                'size':size
        }
        url='/api/v1/kline.do'
        return api_key_get(params, url)


    # 我的钱包
    def wallet_info(self):
        params={}
        url='/api/v1/wallet_info.do'
        return api_key_post(params, url)


    # 用户的订单信息
    # id=-1时，查询未成交的订单
    def order_info(self, symbol, order_id=-1):
        params={
                'symbol':symbol,
                'order_id':order_id
        }
        url='/api/v1/order_info.do'
        return api_key_post(params, url)

    # 单笔撤单
    def cancel_order(self, symbol, order_id):
        params = {
            'symbol':symbol,
            'order_id':order_id
        }
        url = '/api/v1/cancel_order.do'
        response = api_key_post(params, url)
        if 'False' == response['result']:
            print("订单 %d 撤单失败，正在重新撤单.."%order_id)
            time.sleep(1.5)
            response = api_key_post(params, url)
        else:
            print("撤单成功")
        print(response)



    # x天内的平均最低成交价
    # 返回X天的最低均价，统计开始的时间，统计结束的时间
    # 默认取最低价3;收盘价4
    def average(self, symbol, x, type=3):
        price_list=self.kline(symbol, '1day', x)
        low_list = []
        num = 0
        for i in range(x):
            low_list.append(price_list[i][type])
            num += float(price_list[i][type])
        num = num / x
        start = self.time_change(price_list[0][0 ])
        end = self.time_change(price_list[x-1][0])
        return (num,start,end)
        
    
    # 将查询到的平均价写入文件    
    def write_average(self, symbol, x): 
        info_tuple = self.average_low(symbol, x)
        print(info_tuple)
        open_file = open('./file/price.txt','a',encoding='utf-8')
        open_file.write(str(x) + "天平均最低价:" + str(info_tuple[0]) + '\n')
        open_file.write(
            "统计起始日期:" +
            str(info_tuple[1]) + 
            "结束日期:" +
            str(info_tuple[2]) + 
            '\n'
            )
        open_file.close()


    # unix时间戳转换，OK精度为毫秒，需要换算成秒
    def time_change(self, timestamp):
        time_second = timestamp/1000
        time_local = time.localtime(time_second)
        date = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        return date

    # 下单
    def trade(self, symbol, type, price, amount):
        params = {
            'symbol':symbol,
            'type':type,
            'price':price,
            'amount':amount,
        }
        url = '/api/v1/trade.do'
        response = api_key_post(params, url)
        # 请求出错，报错
        if not response:
            print("下单失败，请检查代理网络")
            return False 
        open_file = open(r'file\\trade.txt','a')
        open_file.write(str(datetime.datetime.now()) + '-->')
        open_file.write(symbol +'  '+ type +':'+ str(price) + '  amount:'+ str(amount) + '  ID:' + str(response['order_id']) + '\n')
        open_file.close()
        return response

    # 获取账户中某个币种的余额
    # free:可用余额
    # freezed:冻结数量
    def wallet_balance(self, type, symbol):
        info = self.get_user_info()['info']['funds'][type][symbol]
        print(info)

    # 某币种的余额：冻结和非冻结
    def token_balance(self,token):
        info = self.get_user_info()
        free_info = info['info']['funds']['free']
        freezed_info = info['info']['funds']['freezed']
        free_balance = free_info[token]
        freezed_balance = freezed_info[token]
        print("%s可用余额:%s 冻结余额:%s"%(token,free_balance,freezed_balance))
        return (free_balance,freezed_balance)

    # 计算买单价 默认平均低价是10天
    def buy_price(self, symbol ,day=10):
        average = self.average(symbol, day)[0]
        # 最近2天的收盘均价
        two_average = self.average(symbol, 2, 4)[0]
        """
        价格调整策略下版本再升级，暂时沿用10天最低均价！
        """
        return round(average,6)

    # 计算购买的数量
    # base:定价币，暂时用usdt作为基本定价币
    def buy_amount(self,symbol,base='usdt'):
        usd_num = self.token_balance(base)
        buy = self.buy_price(symbol)
        print(usd_num)
        print(round(float(usd_num),4))
        #减掉10，避免下单失败
        amount = float(usd_num) / buy -10
        return int(amount)


    # 当前持仓占总金额比
    """
    已用定价币数量 = （某币种冻结数量+某币种未冻结数量）* 某币种当前成交价 + 冻结定价币
    当前定价币已用百分比= 已用 /（剩余未冻结定价币数量+已用定价币数量）
    symbol:某币交易对
    token:某币名称
    base:定价币名称
    """
    def proportion(self, symbol, token, base='usdt'):
        (usd_free, usd_freezed) = self.token_balance(base)
        (symbol_freezed, symbol_free) = self.token_balance(token)
        symbol_price = self.average(symbol, 1, 4)[0]
        used = (float(symbol_freezed) + float(symbol_free)) * symbol_price + float(usd_freezed)
        # 定价币总量
        total = float(usd_free) + used
        # 当前定价币已用百分比
        present = used / total * 100
        print("%s已用%s 当前已用比例:%s%%"%(base,used,round(present,6)))
        return (round(present,6),total)

    def update_key(self, api_key, secret_key):
        read_ini = ReadIni()
        read_ini.set_value('api_key',api_key)
        read_ini.set_value('secret_key',secret_key)
        return True


if __name__ == '__main__':
    run = RunMethod()
    run.proportion('show_usdt','show')
 #   run.buy_price("show_usdt", 10)