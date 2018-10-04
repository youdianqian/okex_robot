#coding=utf-8
import sys
sys.path.append(r'G:\gui_exchange\base')
from method import RunMethod
from config.find_config import ReadIni
import time
import datetime

# 网格交易V0.1
"""
    1.拿到X天内的平均最低价
    2.买单价=最低价+-(最近2天收盘价)*0.08
    2.检查当前挂单，撤掉低于X天均价的单
    3.统计账户余额
    4.按10%半仓，20%3成仓，30%空仓挂卖单
    5.循环检测是否有成交单，重新挂买单 
""" 
class Main(object):
    def __init__(self):
        self.run = RunMethod()

    # 拿到买价，检测当前挂单，高于计算买价的都撤掉
    def alfa(self,symbol ,day):
        order = self.run.order_info(symbol)['orders']
        num = len(order)
        cancel_id = []
        if num > 0:
            for i in range(num):    
                cancel_id.append(order[i]['order_id'])
            for i in range(len(cancel_id)):
                self.run.cancel_order(symbol, cancel_id[i])
                print("撤单结束")
                return  
        else:
            print("当前没有挂单")
            return True


    """
    买入规则：
    70%仓位--->平均价
    70-90%仓位-->低于均价7%
    90-100%仓位->低于均价13%
    下单数量：show最低下单量为10个，没有小数位,为了避免下单失败，下单量都减1
    """
    def buy(self, symbol, token, day):
        average = self.run.buy_price(symbol)
        while True:
            time.sleep(1)
            (proportion,total) = self.run.proportion(symbol, token)
            if proportion < 70:
                price = average
                amount = (71 - proportion) / 100 * total / average 
                response = self.run.trade(symbol, 'buy', price, int(amount) - 1)
            elif 70 <= proportion < 90:
                price = average * 0.93
                # 因为计算精度问题，这个区间多挂一个点的单，避免出现持仓89.999%，导致下次挂单量过少失败。
                amount = (91 - proportion) / 100 * total / price                
                response = self.run.trade(symbol, 'buy', price, int(amount) - 1)
            elif 90 <= proportion < 99:
                price = average * 0.87
                amount = (100 - proportion) / 100 * total / price 
                response = self.run.trade(symbol, 'buy', price, int(amount) - 1)
                print("挂买单成功，买入币种%s 买入价格:%s 买入数量%s"%(token,price,int(amount)-1))
                return
            else:
                print("可用余额不足，没有挂买单")
                return
            if not response:
                print("代理网络报错，正在检查是否挂单成功..")
            else:
                print("挂买单成功，买入币种%s 买入价格:%s 买入数量%s"%(token,price,int(amount)-1))

    #挂卖单
    """
    1.检测是否有该币种的余额
    2.如果大于10个就可以下单，show的最低下单量是10个
    3.按余额的比例挂卖
    50% 110%
    80% 120%
    100% 130%
    """
    def sell(self, symbol, token, day):
        average = self.run.buy_price(symbol)
        while True:
            (free_balance,freezed_balance) = self.run.token_balance(token)
            total = float(free_balance) + float(freezed_balance)
            usd_amount = float(self.run.proportion(symbol, token)[1])
            token_proportion = total / usd_amount * average
            print(token_proportion)
            if round(float(free_balance)) > 10:
                if token_proportion < 50:
                    price = average * 1.1
                    response = self.run.trade(symbol, 'sell', price,round(float(free_balance)) - 1)
                elif 50 <= token_proportion < 80:
                    price = average * 1.2
                    # 因为计算精度问题，这个区间多挂一个点的单，避免出现持仓79.999%，导致下次挂单量过少失败。           
                    response = self.run.trade(symbol, 'buy', price, round(float(free_balance)) - 1)
                elif 80 <= token_proportion < 99:
                    price = average * 1.3        
                    response = self.run.trade(symbol, 'buy', price, round(float(free_balance)) - 1)
                    print("挂卖单成功，卖出币种%s 卖出价格:%s 卖出数量%s"%(token,price,int(free_balance)-1))
                    return
                else:
                    print("可用余额不足，没有挂卖单")
                    return
                if not response:
                    print("代理网络报错，正在检查是否挂单成功..")
                else:
                    print("挂卖单成功，卖出币种%s 卖出价格:%s 卖出数量%s"%(token,price,round(float(free_balance)) - 1))
            else:
                print("定价币余额不足，挂卖单失败")
                return 


    # 下单并记录在read.txt中
    def main(self, symbol=None, token=None, day=None, flag=None):
        while True:
        # self.alfa(symbol, day)
            self.buy(symbol, token, day)
            self.sell(symbol, token, day)
            now = datetime.datetime.now()
            print("本次执行完成时间:%s ，一小时后再次循环执行"%now)
            time.sleep(3600)

    def update_key(self, api_key, secret_key):
        if self.run.update_key(api_key, secret_key):
            return True        
        else:
            return False
        





if __name__ == '__main__':
    run = Main()
    run.alfa('show_usdt', 10)
  #  run.buy('show_usdt', 'show', 10)
 #   run.alfa('show_usdt', 10)