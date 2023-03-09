import os
import pandas as pd
from configurations import setup_logger, basic_parameters as bp
from multiprocessing import Pool, cpu_count

logger = setup_logger('read_csvs')

names = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']



#----- Lists of files 

csv_dir = '../big_dataframes/binance/spot/daily/klines/BTCUSDT/1s/'
theOrderBookFiles = sorted(os.listdir(csv_dir))

def read_csv_inparalel(file):
    return pd.read_csv(csv_dir+file, names=names, usecols=['Open time', 'Open', 'High', 'Low', 'Close'])
    

logger.info('start read csvs')
with Pool(cpu_count()) as p:
    files = p.map(read_csv_inparalel, theOrderBookFiles)
logger.info('finish read csvs')

df = pd.concat(files, ignore_index = True)


logger.info(df.shape)

def computeRSI (data, time_window):
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi


def stochastic(data, k_window, d_window, window):
    
    # input to function is one column from df
    # containing closing price or whatever value we want to extract K and D from
    
    min_val = data.rolling(window=window, center=False).min()
    max_val = data.rolling(window=window, center=False).max()
    
    stoch = ( (data - min_val) / (max_val - min_val) ) * 100
    
    K = stoch.rolling(window=k_window, center=False).mean() 
    #K = stoch
    
    D = K.rolling(window=d_window, center=False).mean() 


    return K, D

df['RSI'] = computeRSI(df['Close'], 14)
df['K'], df['D'] = stochastic(df['RSI'], 3, 3, 14)

df['time UTC'] = pd.to_datetime(df['Open time'], unit='ms', origin='unix')
df.dropna(inplace=True)
#df

stochastic_value = 0
RSI_value = 20
df.loc[(df['D'] <= stochastic_value) & (df['RSI'] <= RSI_value), 'buy?'] = True
#df.loc[df['D'] <= stochastic_value, 'buy?'] = True
#df.loc[df['buy?'] == True]

rolling_seconds = 60

df['min_val'] = df['Low'].shift(-rolling_seconds).rolling(window=rolling_seconds).min()
df['max_val'] = df['High'].shift(-rolling_seconds).rolling(window=rolling_seconds).max()

df['max_val_%'] = (df['max_val'] - df['Open'].shift(-1)) * 100 / df['Open'].shift(-1)
df['min_val_%'] = (df['min_val'] - df['Open'].shift(-1)) * 100 / df['Open'].shift(-1)

#df.dropna(inplace=True)
#df[60:70]
#df.loc[df['buy?'] == True]

df = df.loc[df['buy?'] == True]
#df = df.loc[df['Open time'] - df['Open time'].shift(1) < rolling_seconds * 1000] # wait for confirmation
#df = df.loc[df['Open time'] - df['Open time'].shift(1) < rolling_seconds * 1000] # wait for 2d confirmation
#df = df.loc[df['Open time'] - df['Open time'].shift(1) < rolling_seconds * 1000] # wait for 3d confirmation
#df = df.loc[df['Open time'] - df['Open time'].shift(1) < rolling_seconds * 1000] # wait for 4d confirmation
df = df.loc[df['Open time'] - df['Open time'].shift(1) > rolling_seconds * 1000] # wait until trade 

tp_size = 0.075
sl_size = 0.075
# 0.075 RSI 40 total profit 2.47

sl = df.loc[(df['buy?'] == True) & (df['min_val_%'] < -sl_size)]
#sl = sl.loc[sl['Open time'] - sl['Open time'].shift(1) > rolling_seconds * 1000]
#sl

tp = df.loc[(df['buy?'] == True) & (df['max_val_%'] > tp_size)]
#tp = tp.loc[tp['Open time'] - tp['Open time'].shift(1) > rolling_seconds * 1000]
#tp




logger.info(f'\n\
tp/sl: {tp.shape[0]/sl.shape[0]} \n\
stochastic_value: {stochastic_value} \n\
RSI_value: {RSI_value} \n\
rolling_seconds: {rolling_seconds} \n\
tp.shape[0]: {tp.shape[0]} || sl.shape[0]: {sl.shape[0]} \n\
total profit % {(tp.shape[0] * tp_size) - (sl.shape[0] * sl_size)}')
