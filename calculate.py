import pandas as pd
import os
import math
def calculate_ret(n, stk_dict):
    # 用开盘价计算所有股票的n日收益率
    # 输入：当前日期，反转天数，股票列表
    # 作用效果：：在股票列表中加入n日收益率这一项
    for name,df in stk_dict.items():
        df_shifted = df.shift(n)
        df['ret'] = (df['open'] - df_shifted['open']) / df['open']

def calculate_benchmark_rate(stk_dict,start_date, end_date,trading_days):
    start_price = 0
    end_price = 0
    while start_date not in trading_days:
        start_date = start_date + pd.DateOffset(days=1)
    while end_date not in trading_days:
        end_date = end_date - pd.DateOffset(days=1)
    for name, df in stk_dict.items():
        start_price += df[df['date']==start_date]['open'].item()
        end_price += df[df['date']==end_date]['open'].item()

    return end_price/start_price

def calculate_year_diff(date_early,date_late):
    """计算两个日期之间差了多少年（没考虑闰年）"""
    years_diff = date_late.year - date_early.year
    days_diff = date_late.day_of_year - date_early.day_of_year
    diff = years_diff + days_diff/365
    return diff

def calculate_annualized_volatility(asset_curve_list):
    daily_return = [math.log(asset_curve_list[i]/asset_curve_list[i-1]) for i in range(1,len(asset_curve_list))]
    mean = sum(daily_return) / len(daily_return)
    variance = sum((x - mean) ** 2 for x in daily_return) / (len(daily_return)-1)
    s = math.sqrt(variance)
    return math.sqrt(252)*s

if __name__ == '__main__':
    start_date = pd.Timestamp(year=2022, month=10, day=1)
    end_date = pd.Timestamp(year=2022, month=11, day=5)
