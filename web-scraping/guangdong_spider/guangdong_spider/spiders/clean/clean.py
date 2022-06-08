import pandas as pd

df = pd.read_csv('./guangdong.csv')

# Sort date 
df = df.sort_values(by = 'Date')

def get_return(df):
   """
   get return time series
   
   param:
   df: dataframe
   """
   
   df['Return'] = df['Return'] * 0.01
   
   return df


get_return(df).to_csv('guangdong_GDEA.csv')