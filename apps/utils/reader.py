import pandas as pd
import fastparquet
import datetime
import requests_cache
from eod_historical_data import get_eod_data
pd.set_option("max_rows", 10)

expire_after = datetime.timedelta(days=10)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)


def get_quotes(tickers, exchange='US'):
    port = []
    port_pct = []
    for ticker in tickers:
        df = get_eod_data(ticker, exchange,  start="2010-01-01", end="2021-01-01", session=session)
        port.append(df['Close'])
        port_pct.append(df['Close'].pct_change().dropna())
    port = pd.concat(port, axis=1, ignore_index=False)
    port_pct = pd.concat(port_pct, axis=1, ignore_index=False)
    port.columns = tickers
    port_pct.columns = tickers
    port.index = pd.to_datetime(port.index, format="%Y%m%d")  # convert index to DateTime Series
    port_pct.index = pd.to_datetime(port_pct.index, format="%Y%m%d")  # convert index to DateTime Series
    port.index = port.index.to_period('D')  # convert DateTime to Periods
    port_pct.index = port_pct.index.to_period('D')  # convert DateTime to Periods
    return port, port_pct

def get_ind(ticker):
    df = get_eod_data(ticker, 'INDX',  start="2010-01-01", end="2021-01-01", session=session)
    port = df['Close']
    port_pct = df['Close'].pct_change().dropna()
    port.columns = ticker
    port_pct.columns = ticker
    port.index = pd.to_datetime(port.index, format="%Y%m%d")  # convert index to DateTime Series
    port_pct.index = pd.to_datetime(port_pct.index, format="%Y%m%d")  # convert index to DateTime Series
    port.index = port.index.to_period('D')  # convert DateTime to Periods
    port_pct.index = port_pct.index.to_period('D')  # convert DateTime to Periods
    return port, port_pct

# # get_symbols()
# # tickers = ['AAPL','ABBV', 'ABT', 'ACN', 'ADBE', 'AMZN', 'AVGO', 'BAC', 'BRK.A', 'CMCSA', 'COST', 'CRM', 'CSCO', 'CVX', 'DHR', 'DIS', 'FB', 'GOOG', 'HD', 'INTC', 'JNJ', 'JPM', 'KO', 'LLY', 'MA', 'MCD', 'MDT', 'MRK', 'MS', 'MSFT', 'NFLX', 'NKE', 'NVDA', 'ORCL', 'PEP', 'PFE', 'PG', 'PYPL', 'QCOM', 'T', 'TMO', 'TSLA', 'TXN', 'UNH', 'UPS', 'V', 'VZ', 'WFC', 'WMT', 'XOM']
# print(get_quotes(tickers))

# df_market = pd.read_parquet('../data/market.parquet.gzip', engine='fastparquet')
# df_market = pd.read_csv('../data/market.csv', header=0, index_col=0, parse_dates=True)
# df_market.index = pd.to_datetime(df_market.index, format="%Y%m%d") # convert index to DateTime Series
# df_market.index = df_market.index.to_period('D') # convert DateTime to Periods
# print(df_market)