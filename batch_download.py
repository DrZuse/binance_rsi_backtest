import datetime
import pandas as pd

import requests
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool


# 2022-07-08 binance zerofee

links_to_download = []
path_to_save = []
for date in pd.date_range(start="2023-03-03", end="2023-03-07"):
    link = f'https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1s/BTCUSDT-1s-{date.strftime("%Y-%m-%d")}.zip'
    path = f'../big_dataframes/binance/spot/daily/klines/BTCUSDT/1s/BTCUSDT-1s-{date.strftime("%Y-%m-%d")}.zip'
    links_to_download.append(link)
    path_to_save.append(path)
    print(link)
print(links_to_download)
inputs = zip(links_to_download, path_to_save)


def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        r = requests.get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return(url, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)

def download_parallel(args):
    cpus = cpu_count()
    results = ThreadPool(cpus - 1).imap_unordered(download_url, args)
    for result in results:
        print('url:', result[0], 'time (s):', result[1])

download_parallel(inputs)