# from stats.stats import get_stats
# help(get_stats)
# type q to quit
# python3.6
# from stats.stats import Stats
# city_name = Stats(csv_file = ['XXXXXXX.csv','/Users/xuhuili/Desktop/ccm_project/Comparator_indices_07062021.csv'], trading_index = 'tianjin', risk_free = 0.02388, start_date = '2016-01-01', end_date = '2020-12-31')
# city_name.get_stats()


import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

class Stats:
   
   def __init__(self, csv_file = None, trading_index = None, risk_free = None, start_date = None, end_date = None, to_csv = None):
      """
      Get carbon market statistics
   
      params:
      csv_file: [carbon market csv, comparator csv] -> list
      trading_index: name of trading index -> string
      risk_free: risk free rate (The China 1 Year Government Bond has a 2.388% yield.) -> float
      start_date: e.g., '2016-01-01' -> string
      end_date: e.g., '2020-12-31' -> string
      to_csv: whether to convert df, result_df and corr_matrix_d into CSV files 
      """
            
      # Read csv file
      self.carbon_df = pd.read_csv(csv_file[0])
      self.comparator_df = pd.read_csv(csv_file[1])
      
      self.trading_index = trading_index
      
      # Define the risk free rate (The China 1 Year Government Bond has a 2.388% yield.)
      self.risk_free = risk_free
      
      self.start_date = datetime.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
      self.end_date = datetime.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
      self.month = abs(self.end_date.month - self.start_date.month) + 1
      if self.end_date.month < self.start_date.month:
         self.years = self.end_date.year - self.start_date.year - 1
      else:
         self.years = self.end_date.year - self.start_date.year
      self.months = self.years * 12 + self.month
      
      self.to_csv = to_csv
   
   def get_stats(self):
      
      # Extract comparator price and return time series
      comparator_df = self.comparator_df[['Date', 'MSCI World Index TR',\
       'Barclays Global Aggregate Bond Index TR', 'Bloomberg Commodity Index TR', 'S&P 500 Total Return Index']]
      # comparator_return_df = self.comparator_df.iloc[:, [0, 5, 6, 7, 8]]
      
      comparator_df['MSCI World Index TR Return'] = comparator_df['MSCI World Index TR'] / comparator_df['MSCI World Index TR'].shift(1)
      comparator_df['Barclays Global Aggregate Bond Index TR Return'] = comparator_df['Barclays Global Aggregate Bond Index TR'] / comparator_df['Barclays Global Aggregate Bond Index TR'].shift(1)
      comparator_df['Bloomberg Commodity Index TR Return'] = comparator_df['Bloomberg Commodity Index TR'] / comparator_df['Bloomberg Commodity Index TR'].shift(1)
      comparator_df['S&P 500 Total Return Index Return'] = comparator_df['S&P 500 Total Return Index'] / comparator_df['S&P 500 Total Return Index'].shift(1)
      comparator_df = comparator_df.loc[(comparator_df['Date'] >= str(self.start_date)) & (comparator_df['Date'] <= str(self.end_date))].reset_index()
   
      # Select time series timeframe of interest
      df = self.carbon_df.loc[(self.carbon_df['Date'] >= str(self.start_date)) & (self.carbon_df['Date'] <= str(self.end_date))].reset_index()
   
      # Merge carbon market dataframe and comparator dataframe (left join)
      df = df.merge(comparator_df, how = 'left', on = 'Date')
      
      print(self.trading_index +  ' carbon market metrics from ' + str(self.start_date) + ' to ' + str(self.end_date))
   
      # Total return 
      total_return = (df.loc[len(df)-1, 'Settlement Price (yuan/ton)'] - df.loc[0, 'Settlement Price (yuan/ton)']) / df.loc[0, 'Settlement Price (yuan/ton)']
      total_return_MSCI = (comparator_df.loc[len(comparator_df)-1, 'MSCI World Index TR'] - comparator_df.loc[0, 'MSCI World Index TR']) / comparator_df.loc[0, 'MSCI World Index TR']
      total_return_Bond = (comparator_df.loc[len(comparator_df)-1, 'Barclays Global Aggregate Bond Index TR'] - comparator_df.loc[0, 'Barclays Global Aggregate Bond Index TR']) / comparator_df.loc[0, 'Barclays Global Aggregate Bond Index TR']
      total_return_Commodity = (comparator_df.loc[len(comparator_df)-1, 'Bloomberg Commodity Index TR'] - comparator_df.loc[0, 'Bloomberg Commodity Index TR']) / comparator_df.loc[0, 'Bloomberg Commodity Index TR']
      total_return_SP500 = (comparator_df.loc[len(comparator_df)-1, 'S&P 500 Total Return Index'] - comparator_df.loc[0, 'S&P 500 Total Return Index']) / comparator_df.loc[0, 'S&P 500 Total Return Index']
      print('>> Total Return: ', str(round(total_return * 100,4)) + '%')
            
      # Calculate the annualised return over months (Yearly rate of return inferred from any time period)
      annualised_return_month = ((1 + total_return) ** (12/self.months)) - 1
      annualised_return_month_MSCI = ((1 + total_return_MSCI) ** (12/self.months)) - 1
      annualised_return_month_Bond = ((1 + total_return_Bond) ** (12/self.months)) - 1
      annualised_return_month_Commodity = ((1 + total_return_Commodity) ** (12/self.months)) - 1
      annualised_return_month_SP500 = ((1 + total_return_SP500) ** (12/self.months)) - 1
      print('>> Annualised return over months: ', str(round(annualised_return_month * 100,4)) + '%')
   
      # Calculated the annualised return over years (Yearly rate of return inferred from any time period) 
      annualised_return_year = ((1 + total_return) ** (1/self.years)) - 1
      annualised_return_year_MSCI = ((1 + total_return_MSCI) ** (1/self.years)) - 1
      annualised_return_year_Bond = ((1 + total_return_Bond) ** (1/self.years)) - 1
      annualised_return_year_Commodity = ((1 + total_return_Commodity) ** (1/self.years)) - 1
      annualised_return_year_SP500 = ((1 + total_return_SP500) ** (1/self.years)) - 1
      print('>> Annualised return over years: ', str(round(annualised_return_year * 100, 4)) + '%')
   
      # Calculate cumulative returns
      daily_cum_ret = (1 + df.loc[:, ['Return']]).dropna().cumprod()
      # print('>> Cumulative return: ', daily_cum_ret.iloc[len(daily_cum_ret) - 1, 0])
   
      # Standard deviation
      std = df['Return'].std()
      std_MSCI = comparator_df['MSCI World Index TR Return'].std()
      std_Bond = comparator_df['Barclays Global Aggregate Bond Index TR Return'].std()
      std_Commodity = comparator_df['Bloomberg Commodity Index TR Return'].std()
      std_SP500 = comparator_df['S&P 500 Total Return Index Return'].std()
      print('>> Standard Deviation: ', round(std, 4))
      
      # Calculate the Sharpe Ratio
      # Calculate the annualised standard deviation 
      annualised_vol = std * np.sqrt(250)
      annualised_vol_MSCI = std_MSCI * np.sqrt(250)
      annualised_vol_Bond = std_Bond * np.sqrt(250)
      annualised_vol_Commodity = std_Commodity * np.sqrt(250)
      annualised_vol_SP500 = std_SP500 * np.sqrt(250)
      print('>> Annualised volatility: ', round(annualised_vol,4))   

      # Calculate the sharpe ratio 
      sharpe_ratio = (annualised_return_year - self.risk_free) / annualised_vol
      print('>> Sharpe ratio: ', round(sharpe_ratio,4))
   
      # Skewness
      skew = df['Return'].skew()
      skew_MSCI = comparator_df['MSCI World Index TR Return'].skew()
      skew_Bond = comparator_df['Barclays Global Aggregate Bond Index TR Return'].skew()
      skew_Commodity = comparator_df['Bloomberg Commodity Index TR Return'].skew()
      skew_SP500 = comparator_df['S&P 500 Total Return Index Return'].skew()
      print('>> Skewnesss: ', round(skew,4))
   
      # Kurtosis
      kurt = df['Return'].kurtosis()
      kurt_MSCI = comparator_df['MSCI World Index TR Return'].kurtosis()
      kurt_Bond = comparator_df['Barclays Global Aggregate Bond Index TR Return'].kurtosis()
      kurt_Commodity = comparator_df['Bloomberg Commodity Index TR Return'].kurtosis()
      kurt_SP500 = comparator_df['S&P 500 Total Return Index Return'].kurtosis()
      print('>> Kurtosis: ', round(kurt,4))
         
      # Construct a covariance matrix for the daily return data
      cov_matrix_d = (df.loc[:, ['Return', 'MSCI World Index TR Return', 'Barclays Global Aggregate Bond Index TR Return', \
      'Bloomberg Commodity Index TR Return', 'S&P 500 Total Return Index Return']].cov()) *250
      # display(cov_matrix_d)

      # Construct a correlation matrix for the daily return data
      corr_matrix_d = round(df.loc[:, ['Return', 'MSCI World Index TR Return', 'Barclays Global Aggregate Bond Index TR Return', \
      'Bloomberg Commodity Index TR Return', 'S&P 500 Total Return Index Return']].corr(), 3)
      # display(corr_matrix_d)
   
      # Calculate the variance with the formula
      weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2]) # equal weighted 
      port_variance = np.dot(weights.T, np.dot(cov_matrix_d, weights))
      port_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix_d, weights)))
      # print('>> Equal weighted portfolio variance: ', str(round(port_variance, 3) * 100) + '%')
      # print('>> Equal weighted portfolio standard deviation: ', str(round(port_stddev, 3) * 100) + '%')
      
      f1 = plt.figure(figsize=(10, 8))
      plt.plot(pd.to_datetime(df['Date']), df['Return'])
      plt.title(self.trading_index + "'s return from " + str(self.start_date) + " to " + str(self.end_date))
      plt.ylabel('return')
      plt.xlabel('date')
      
      f2 = plt.figure(figsize=(10, 8))
      plt.hist(df['Return'].dropna(), bins = 10, density = False)
      plt.title('Histogram plot of daily returns')
      plt.ylabel('frequency')
      plt.xlabel('return')
      
      df = df.set_index('Date')
      
      f3 = plt.figure(figsize=(10, 8))
      # Calculate cumulative returns
      daily_cum_ret = (1 + df.loc[:, ['Return']]).dropna().cumprod()
   
      # Plot cumulative return 
      daily_cum_ret.Return.plot(title = 'Cumulative Return Plot')
      
      # Calculate the maximum value of returns over 180 days (half-year period) using rolling().max() 
      roll_max = df['Settlement Price (yuan/ton)'].rolling(min_periods = 1, window = 180).max()
      
      # Calculate daily draw-down from rolling max
      daily_drawdown =  df['Settlement Price (yuan/ton)'] / roll_max - 1.0
      
      # Calculate maximum daily draw-down over 180 days (half-year period)
      max_daily_drawdown = daily_drawdown.rolling(min_periods = 1 ,window = 180).min()
      print('>> Maximum drawdown: ', str(min(round(max_daily_drawdown * 100, 2))) + '%')
      
      f4 = plt.figure(figsize=(10, 8))
      # Plot the results 
      daily_drawdown.plot(label = 'Daily drawdown')
      max_daily_drawdown.plot(label = 'Maximum daily drawdown in time-window')
      plt.legend(loc="lower left")
      plt.title('Maximum daily drawdown (window length = 180 days)')
      
      plt.show()
            
      # Construct results dataframes for both carbon market index and comparator indices
      result_df = pd.DataFrame({'Total Return': [round(total_return,4), round(total_return_MSCI,4), round(total_return_Bond,4), \
      round(total_return_Commodity,4), round(total_return_SP500,4)], 
                                 'Annualised return over months': [round(annualised_return_month,4), \
                                 round(annualised_return_month_MSCI,4), round(annualised_return_month_Bond,4), round(annualised_return_month_Commodity,4), \
                                 round(annualised_return_month_SP500,4)],
                                 'Annualised return over years': [round(annualised_return_year, 4), round(annualised_return_year_MSCI, 4), round(annualised_return_year_Bond, 4),\
                              round(annualised_return_year_Commodity, 4), round(annualised_return_year_SP500, 4)],
                                 'Standard Deviation': [round(std, 4), round(std_MSCI, 4), round(std_Bond, 4), round(std_Commodity, 4), round(std_SP500, 4)], 
                                 'Skewnesss': [round(skew,4), round(skew_MSCI,4), round(skew_Bond,4), round(skew_Commodity,4), round(skew_SP500,4)], 
                                 'Kurtosis': [round(kurt,4), round(kurt_MSCI,4), round(kurt_Bond,4), round(kurt_Commodity,4), round(kurt_SP500,4)],
                                 'Annualised volatility': [round(annualised_vol,4), round(annualised_vol_MSCI,4), round(annualised_vol_Bond,4), round(annualised_vol_Commodity,4), round(annualised_vol_SP500,4)],
                                 'Sharpe ratio': [round(sharpe_ratio,4), None, None, None, None], 
                                 }, index = [self.trading_index, 'MSCI World Index TR', 'Barclays Global Aggregate Bond Index TR', \
                              'Bloomberg Commodity Index TR', 'S&P 500 Total Return Index']) 
      
      df = df.reset_index()          
      
      # Export df, result_df and corr_matrix_d as CSV files.
      if self.to_csv:
         df.loc[:, 'Date':'S&P 500 Total Return Index Return'].to_csv('stats_output/' + self.trading_index + '_aggregated_df_' + str(self.start_date) + '_' + str(self.end_date) + '.csv')
         result_df.to_csv('stats_output/' + self.trading_index + '_result_df_' + str(self.start_date) + '_' + str(self.end_date) + '.csv')
         corr_matrix_d.to_csv('stats_output/' + self.trading_index + '_correlation_' + str(self.start_date) + '_' + str(self.end_date) + '.csv')


class Correlation:
   
   def __init__(self, csv_files, start_date, end_date, to_csv):
      """
      Get correlation of Chinese carbon markets over pre-specified timeframe
   
      params:
      csv_files: [carbon market csv1, carbon market csv2, ...] -> list of 8 Chinese carbon market CSV files
      in the following order: 'Beijing', 'Chongqing', 'Fujian', 'Guangdong', 'Hubei', 'Shanghai', 'Shenzhen', 'Tianjin'
      start_date: e.g., '2016-01-01' -> string
      end_date: e.g., '2020-12-31' -> string
      to_csv: whether to convert correlation matrix into CSV file 
      """
      self.start_date = datetime.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
      self.end_date = datetime.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
      self.csv_files = csv_files
      self.to_csv = to_csv
      
   
   def get_correlation(self):
      
      # Aggregated returns of different Chinese carbon market into a dataframe
      df = pd.DataFrame()
      
      for csv in self.csv_files:
         df_cm = pd.read_csv(csv)
         df = pd.concat([df, df_cm['Return']], axis = 1)
         
      # Rename columns 
      df.columns = ['Beijing', 'Chongqing', 'Fujian', 'Guangdong', 'Hubei', 'Shanghai', 'Shenzhen', 'Tianjin']
         
      # Construct a correlation matrix for alldifferent Chinese carbon market
      corr_matrix_d = round(df.corr(), 3)
      
      if self.to_csv:
         corr_matrix_d.to_csv('stats_output/' + 'Chinese_carbon_market_correlation_' + str(self.start_date) + '_' + str(self.end_date) + '.csv')
         
      
      




         