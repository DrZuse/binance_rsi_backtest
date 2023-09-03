# Binance Historical Data Downloader

`batch_download.py` - this Python script allows you to download historical spot trading data for the BTCUSDT trading pair on Binance. The data is downloaded in ZIP format for one-second intervals for a specified date range.

## Usage

1. Make sure you have the required Python libraries installed. You can install them using pip:

   ```bash
   pip install pandas requests
   ```

2. Clone or download this repository to your local machine.

3. Modify the script to specify the date range and file paths for downloading and saving the data:

   ```python
   # Define the date range for data download
   start_date = "2023-03-07"
   end_date = "2023-03-13"

   # Define the directory where you want to save the downloaded data
   save_directory = "../big_dataframes/binance/spot/daily/klines/BTCUSDT/1s/"
   ```

4. Run the script:

   ```bash
   python download_binance_data.py
   ```

   The script will print the URLs it is downloading and the time taken for each download.

## Script Details

- The script uses the `requests` library to download data from Binance's data API.
- It utilizes multithreading with `ThreadPool` to download data in parallel, taking advantage of your CPU's capabilities.
- The downloaded data is saved as ZIP files in the specified directory.

## Note

- Make sure you have a stable internet connection while running the script as it relies on internet connectivity to download data.
- The script will download data for each day in the specified date range, so ensure that you have sufficient disk space available for storing the downloaded ZIP files.

Feel free to modify the script according to your requirements and use it to collect historical trading data from Binance.


# Trading Strategy Analyzer

`multi_backtest.py` - this Python script is designed to analyze a trading strategy using historical cryptocurrency price data from Binance. The script performs the following steps:

1. **Import Required Libraries:**
   - `os`: Operating system interactions.
   - `pandas`: Data manipulation and analysis.
   - `setup_logger`: Custom function for setting up logging.
   - `basic_parameters`: Custom module for basic configuration parameters.
   - `Pool` and `cpu_count` from `multiprocessing` for parallel processing.

2. **Define Constants:**
   - `names`: A list of column names used when reading CSV files.
   - `csv_dir`: The directory containing the historical price data files.

3. **Read Historical Price Data in Parallel:**
   - The script reads multiple CSV files in parallel using the `multiprocessing` library to speed up data loading.

4. **Calculate RSI (Relative Strength Index):**
   - The `computeRSI` function calculates the RSI indicator for the historical price data.

5. **Calculate Stochastic Oscillator (K and D values):**
   - The `stochastic` function calculates the stochastic oscillator values (K and D) for the RSI data.

6. **Data Preprocessing:**
   - The script converts timestamps to datetime format and drops rows with missing data.

7. **Generate Buy Signals:**
   - Buy signals are generated based on specific conditions related to the Stochastic Oscillator (D) and RSI values.

8. **Define Rolling Time Periods:**
   - Rolling time periods are defined for calculating minimum and maximum values of price changes.

9. **Filter Buy Signals:**
   - Buy signals are filtered based on specific conditions, such as waiting for confirmation and trade intervals.

10. **Calculate Take Profit (TP) and Stop Loss (SL):**
    - The script calculates take profit and stop loss levels based on predefined criteria.

11. **Display Analysis Results:**
    - The script logs various analysis results, including the ratio of TP to SL signals, parameter values, and total profit percentage.

## Usage

To use this script, follow these steps:

1. Place your historical price data CSV files in the `csv_dir` directory.
2. Update the script with your preferred strategy parameters, such as `stochastic_value`, `RSI_value`, `rolling_seconds`, `tp_size`, and `sl_size`.
3. Run the script.

The script will analyze the trading strategy and provide insights into its performance based on the provided parameters.

**Note:** Ensure that you have the required dependencies and data files before running the script.


# Trading Strategy using RSI Indicator

`numpy_backtest.py` - this Python script is designed to implement a trading strategy based on the Relative Strength Index (RSI) indicator. It replaces the use of the Pandas library with Numpy for data manipulation and allows you to change the number of consecutive RSI lows required for a trading signal. The script reads historical price data from CSV files, calculates RSI values, and identifies potential trade signals based on specified RSI thresholds.

## Requirements

Before running the script, make sure to install the required packages:

- Cython
  ```
  pip install Cython
  ```

- qtalib
  ```
  pip install qtalib
  ```

## Usage

1. Clone the repository or download the script to your local machine.

2. Set up your directory structure and update the `csv_dir` variable to point to the directory containing your CSV files with historical price data.

3. Customize the RSI threshold by modifying the `rsi_value` variable. The default value is 25.

4. Adjust your trading parameters by modifying the following variables:
   - `profit_percent`: Desired profit percentage for closing a trade.
   - `loss_percent`: Maximum tolerable loss percentage for closing a trade.

5. Run the script.

6. The script will calculate RSI values, identify potential trading signals, and output various statistics, including profitable trades, losing trades, trade ratios, and more.

## Important Notes

- The script assumes that your CSV files have the following columns: 'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'.

- The script uses multi-processing for reading CSV files in parallel to improve efficiency. The number of CPU cores used for parallel processing is determined by `cpu_count()`.

- The script calculates RSI values and looks for trading signals based on consecutive RSI lows. The trading strategy is based on the RSI indicator, and you can adjust the RSI threshold and trading parameters to suit your needs.

- The script provides statistics on profitable trades, losing trades, trade ratios, unfinished trades, and more.

## Disclaimer

This script is for educational and demonstration purposes only. It does not constitute financial advice, and using it for actual trading carries risks. Before implementing any trading strategy, thoroughly research and backtest it using historical data. Additionally, consider consulting with a financial advisor or conducting your own analysis before making any financial decisions.