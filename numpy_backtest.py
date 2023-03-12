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
#logger.info(rsi_values)
rsi_values[0:14] = None # in respect to irrelevant values
signals = np.where(rsi_values < 25)


#logger.info(signals[0].tolist())
list_of_signals = signals[0].tolist()
logger.info(f'number of signals: {len(list_of_signals)}')


profits = 0
losses = 0
trade_exit = 0
not_finished_trades = 0

profit_percent = 0.05
loss_percent = 0.05

logger.info('start loop')

for s, sig in enumerate(list_of_signals):
    #print(f'current  sig {sig}')
    #print(f'current -1  {sig-1}')
    #print(f'previous {list_of_signals[s-1]}' )
    #print(f'previous {list_of_signals[s-1]}' )
    #print(f'if? {list_of_signals[s-1] == sig-1}' )
    if sig > trade_exit and list_of_signals[s-1] == sig-1:
        logger.info(f'time_of_signal: {datetime.datetime.utcfromtimestamp(big_arr[(sig+1), 0]/1000)}')

        buy_price = big_arr[(sig+1), 1] # open price
        max_high = big_arr[(sig+1), 2]
        max_low = big_arr[(sig+1), 3]
        loss = (buy_price - max_low) * 100 / buy_price
        profit = (max_high - buy_price) * 100 / buy_price
        
        for m, big_arr_m in enumerate(big_arr[(sig+1):]):
        
            if big_arr_m[2] > max_high:
                max_high = big_arr_m[2]
                profit = (max_high - buy_price) * 100 / buy_price

            if big_arr_m[3] < max_low:
                max_low = big_arr_m[3]
                loss = (buy_price - max_low) * 100 / buy_price

            if profit >= profit_percent:
                profits += 1

            if loss >= loss_percent:
                losses += 1

            if profit >= profit_percent or loss >= loss_percent:
                print(f'buy_price: {buy_price}')
                print(f'profit: {profit} || loss: {loss}')
                print(f'max_high: {max_high} || max_low: {max_low}')
                print(f'time of the end a trade: {datetime.datetime.utcfromtimestamp(big_arr_m[0]/1000)}')

                trade_exit = (sig+1) + m

                break
        else:
            not_finished_trades += 1

            
            




        #if i % 30_000 == 0:
        #    logger.info(f'profits: {profits} || loss: {losses} || {datetime.datetime.utcfromtimestamp(big_arr_i[0]/1000)}')

logger.info(f'profitable trades: {profits} - {profits*profit_percent} \n\
lose trades: {losses} - {losses*loss_percent} \n\
not_finished_trades: {not_finished_trades} \n\
profit_percent: {profit_percent} || loss_percent: {loss_percent} \n\
total_profit: {(profits*profit_percent)-(losses*loss_percent)}')

logger.info('finish')
        
