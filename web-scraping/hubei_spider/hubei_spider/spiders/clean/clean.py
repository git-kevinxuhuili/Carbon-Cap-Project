import pandas as pd

df = pd.read_csv('./hubei.csv')

# Sort date 
df = df.sort_values(by = 'Date')

def get_return(df):
   """
   get return time series
   
   param:
   df: dataframe
   """
   
   df['Return'] = df['Settlement Price (yuan/ton)'] / df['Settlement Price (yuan/ton)'].shift(1) - 1
   
   return df

get_return(df).to_csv('hubei_HBEA.csv')