import pandas as pd
import os


def divide_feather(data_path, start_date, end_date):
    """读取feather中没有缺失数据的各个股票，并返回一个字典 stk_id -> dohlc数据"""
    df = pd.read_feather(data_path)
    stk_dict = {}
    while len(df) != 0:
        cur_id = df.iloc[0]['stk_id']
        value = df.loc[:, 'date': 'close'][df['stk_id'] == cur_id]
        if len(value) == 728:
            value = value[(value['date'] >= start_date) & (value['date'] <= end_date)]
            stk_dict[cur_id] = value

        df = df[df['stk_id'] != cur_id]
    return stk_dict


