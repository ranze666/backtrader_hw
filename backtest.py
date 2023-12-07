import pandas as pd
import os
from initialize import divide_feather
from calculate import calculate_ret,calculate_benchmark_rate,calculate_year_diff,calculate_annualized_volatility
from strategy import cross_section_reversion
class Backtest():
    def __init__(self, data_path, start_date, end_date, n, cash):
        self.stk_dict = divide_feather(data_path,start_date,end_date)
        self.start_date = start_date
        self.end_date = end_date
        self.n = n
        self.initial_cash = cash
        self.cash = cash
        self.total_asset = cash
        self.hold_dict = {}
        self.trading_days = self.stk_dict['000001.SZ']['date'].tolist()[n:]
        self.asset_curve_list = []
    def run_trading(self):
        # 计算n日收益率，并存入数据中
        calculate_ret(self.n, self.stk_dict)

        today = self.start_date + pd.DateOffset(days=self.n+1)
        self.asset_curve_list.append(self.total_asset)
        # 通过循环，遍历选定的日期范围
        while today <= self.end_date:
            # 判断今天是不是交易日
            if today in self.trading_days:
                self.cash, self.hold_dict, self.total_asset = cross_section_reversion(self.stk_dict, self.cash, today,self.hold_dict)
                self.asset_curve_list.append(self.total_asset)
            today = today + pd.DateOffset(days=1)

    def output(self):
        benckmark = calculate_benchmark_rate(self.stk_dict,self.start_date, self.end_date,self.trading_days)
        years = calculate_year_diff(self.start_date,self.end_date)
        excess_return_rate = (self.total_asset - self.initial_cash * benckmark) / (self.initial_cash * benckmark)
        annualized_return_rate = ((self.total_asset - self.initial_cash)/self.initial_cash)/years
        annualized_volatility = calculate_annualized_volatility(self.asset_curve_list)
        sharpe_ratio = annualized_return_rate/annualized_volatility
        maximun_drawdown = (max(self.asset_curve_list) - min(self.asset_curve_list))/max(self.asset_curve_list)
        return self.asset_curve_list,excess_return_rate,annualized_return_rate,annualized_volatility,sharpe_ratio,maximun_drawdown
