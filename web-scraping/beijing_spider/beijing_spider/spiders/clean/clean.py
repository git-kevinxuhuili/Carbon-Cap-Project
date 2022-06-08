import pandas as pd

df = pd.read_csv('./beijing.csv')

# Sort date 
df = df.sort_values(by = 'Date')

def get_index_df(df, index = None):
   """
   get dataframe with specific index.
   
   param:
   df: dataframe
   index: trading index
   """
   for i in range(len(df)):
      try:
         df.loc[i, 'Trading Index'] = df.loc[i, 'Turnover (yuan)'].split('(')[1][:-1]
         df.loc[i, 'Turnover'] = df.loc[i, 'Turnover (yuan)'].split('(')[0]
      except IndexError:
         try:
            df.loc[i, 'Trading Index'] = df.loc[i, 'Turnover (yuan)'].split('（')[1][:-1]
            df.loc[i, 'Turnover'] = df.loc[i, 'Turnover (yuan)'].split('（')[0]
         except IndexError:
            df.loc[i, 'Trading Index'] = None
            df.loc[i, 'Turnover'] = df.loc[i, 'Turnover (yuan)']
            
   df_index = df[df['Trading Index'] == index].reset_index().drop(columns = ['Turnover (yuan)', 'index'])
   
   return df_index


def get_return(df):
   """
   get return time series
   
   param:
   df: dataframe
   """
   
   df['Return'] = df['Settlement Price (yuan/ton)'] / df['Settlement Price (yuan/ton)'].shift(1) - 1
   
   return df


df_CCER = get_index_df(df, index = 'CCER')
df_BEA = get_index_df(df, index = 'BEA')
df_null = df[df['Trading Index'].isnull()].reset_index().drop(columns = ['Turnover (yuan)', 'index'])
df_林业碳汇 = get_index_df(df, index = '林业碳汇')


get_return(df_CCER).to_csv('beijing_CCER.csv')
get_return(df_BEA).to_csv('beijing_BEA.csv')
get_return(df_null).to_csv('beijing_.csv')
get_return(df_林业碳汇).to_csv('beijing_林业碳汇.csv')
