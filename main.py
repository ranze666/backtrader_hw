import pandas as pd
import os
from backtest import Backtest

data_path = os.path.join('..','data','stk_daily.feather')
start_date = pd.Timestamp(year=2021,month=10,day=1)
end_date = pd.Timestamp(year=2022,month=11,day=5)
backtest = Backtest(data_path,start_date,end_date,5,100000)
backtest.run_trading()
asset_curve_list,excess_return_rate,annualized_return_rate,annualized_volatility,sharpe_ratio,maximun_drawdown = backtest.output()
print('down')