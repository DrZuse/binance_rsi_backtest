# replace pandas with numpy
# chenge number of RSI's lows in a row


import datetime
import numpy as np
import os
import pandas as pd
import random
import qtalib.indicators as ta # requarements: pip install Cython, pip install qtalib

from configurations import setup_logger, basic_parameters as bp
from multiprocessing import Pool, cpu_count

logger = setup_logger('read_csvs')

names = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']



#----- Lists of files 

csv_dir = '../big_dataframes/binance/spot/daily/klines/BTCUSDT/1s/'
theOrderBookFiles = sorted(os.listdir(csv_dir))

def read_csv_inparalel(file):
    return np.loadtxt(csv_dir+file, delimiter=",", dtype=np.float64, usecols=[0, 1, 2, 3, 4])
    

logger.info('start read csvs')
with Pool(cpu_count()) as p:
    #files = p.map(read_csv_inparalel, theOrderBookFiles)
    files = p.map(read_csv_inparalel, theOrderBookFiles[-3:]) # TEST 3 files
logger.info('finish read csvs')


big_arr = np.concatenate(files, axis=0)

#df['time UTC'] = pd.to_datetime(df['Open time'], unit='ms', origin='unix')

logger.info(big_arr.shape)

rsi_values = ta.RSI(big_arr[:, 4]) # values 1-13 irrelevant

