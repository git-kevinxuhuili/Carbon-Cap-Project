import pandas as pd

df = pd.read_csv('./shenzhen.csv')

# Sort date
df = df.sort_values(by = 'Date')

df_SZA_2013 = df[df['Trading Index'] == 'SZA-2013'].reset_index()
df_SZA_2014 = df[df['Trading Index'] == 'SZA-2014'].reset_index()
df_SZA_2015 = df[df['Trading Index'] == 'SZA-2015'].reset_index()
df_SZA_2016 = df[df['Trading Index'] == 'SZA-2016'].reset_index()
df_SZA_2017 = df[df['Trading Index'] == 'SZA-2017'].reset_index()
df_SZA_2018 = df[df['Trading Index'] == 'SZA-2018'].reset_index()
df_SZA_2019 = df[df['Trading Index'] == 'SZA-2019'].reset_index()
df_SZA_2020 = df[df['Trading Index'] == 'SZA-2020'].reset_index()

def get_return(df):
   """
   get return time series
   
   param:
   df: dataframe
   """
   df['Return'] = df['Settlement Price (yuan/ton)'] / df['Settlement Price (yuan/ton)'].shift(1) - 1
   
   return df
   

get_return(df_SZA_2013).to_csv('shenzhen_SZA_2013.csv')
get_return(df_SZA_2014).to_csv('shenzhen_SZA_2014.csv')
get_return(df_SZA_2015).to_csv('shenzhen_SZA_2015.csv')
get_return(df_SZA_2016).to_csv('shenzhen_SZA_2016.csv')
get_return(df_SZA_2017).to_csv('shenzhen_SZA_2017.csv')
get_return(df_SZA_2018).to_csv('shenzhen_SZA_2018.csv')
get_return(df_SZA_2019).to_csv('shenzhen_SZA_2019.csv')
get_return(df_SZA_2020).to_csv('shenzhen_SZA_2020.csv')
