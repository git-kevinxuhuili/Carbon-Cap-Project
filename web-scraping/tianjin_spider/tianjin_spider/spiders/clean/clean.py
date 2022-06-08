import pandas as pd

df = pd.read_csv('./tianjin.csv')

# Sort date
df = df.sort_values(by = 'Date').reset_index()

df_TJEA20 = df[df['Trading Index'] == 'TJEA20'].reset_index()
df_TJEA19 = df[df['Trading Index'] == 'TJEA19'].reset_index()
df_TJEA18 = df[df['Trading Index'] == 'TJEA18'].reset_index()
df_TJEA17 = df[df['Trading Index'] == 'TJEA17'].reset_index()
df_TJEA16 = df[df['Trading Index'] == 'TJEA16'].reset_index()
df_TJEA15 = df[df['Trading Index'] == 'TJEA15'].reset_index()
df_TJEA14 = df[df['Trading Index'] == 'TJEA14'].reset_index()
df_TJEA13 = df[df['Trading Index'] == 'TJEA13'].reset_index()

def get_return(df):
   """
   get return time series
   
   param:
   df: dataframe
   """   
   
   # Get return time series
   df['Return'] = df['Settlement Price (yuan/ton)'] / df['Settlement Price (yuan/ton)'].shift(1) - 1
   
   return df
   
get_return(df).to_csv('tianjin_.csv')
get_return(df_TJEA20).to_csv('tianjin_TJEA20.csv')
get_return(df_TJEA19).to_csv('tianjin_TJEA19.csv')
get_return(df_TJEA18).to_csv('tianjin_TJEA18.csv')
get_return(df_TJEA17).to_csv('tianjin_TJEA17.csv')
get_return(df_TJEA16).to_csv('tianjin_TJEA16.csv')
get_return(df_TJEA15).to_csv('tianjin_TJEA15.csv')
get_return(df_TJEA14).to_csv('tianjin_TJEA14.csv')
get_return(df_TJEA13).to_csv('tianjin_TJEA13.csv')
