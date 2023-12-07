import operator

import pandas as pd
import os

def cross_section_reversion(stk_dict, cash, today, hold_dict):
    """ 进行买卖操作：卖出手中所有的股票，再买入n日收益率最低的十只股票（分别用现有金额的1/10去买）
        输入：stk_dict，钱，当前日期，当前持仓情况
        输出：钱，持仓情况，总资产
    """
    # 读取当前日期，所有股票的收益率，并存入一个字典
    cur_ret_dict = {name: df[df['date'] == today]['ret'].item() for name, df in stk_dict.items()}
    # 排序,升序排序
    sorted_cur_ret_dict = dict(sorted(cur_ret_dict.items(), key=operator.itemgetter(1)))

    # 卖出操作，卖光所有的股票
    if hold_dict == {}:
        pass
    else:
        for name,count in hold_dict.items():
            df = stk_dict[name]
            price = df[df['date']==today]['open'].item()
            cash += count * price
        hold_dict = {}
    # 记录总资产
    total_asset = cash
    # 买入操作，用现有金额的十分之一去分别买入十只股票
    to_buy = list(sorted_cur_ret_dict.keys())[:10]
    max_cash_per_stk = cash / 10
    for name in to_buy:
        df = stk_dict[name]
        price = df[df['date']==today]['open'].item()
        count = max_cash_per_stk // price
        cash -= count * price
        hold_dict[name] = count
    return cash,hold_dict,total_asset