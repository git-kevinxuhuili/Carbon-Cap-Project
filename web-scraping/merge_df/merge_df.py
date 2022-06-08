import pandas as pd


def merge_df(csv_files = None, comparator_csv = None, to_csv = None):
   
   """
   Merge dataframes of Chinese carbon markets as well as comparator dataframe over pre-specified timeframe

   params:
   csv_files: [carbon market csv1, carbon market csv2, ...] -> list of 8 Chinese carbon market CSV files
   comparator_csv: comparator csv file
   to_csv: whether to convert df into CSV file
   """
   
   # Create an empty dataframe
   df = pd.DataFrame()

   
   # Merge Chinese carbon markets
   for i in range(len(csv_files)):
      
      csv_df = pd.read_csv(csv_files[i])
      
      csv_df = csv_df[['Trading Index', 'Date', 'Settlement Price (yuan/ton)', 'Settlement Volume (ton)']]
            
      df = pd.concat([df, csv_df])
   
   # read comparator CSV file
   comparator_df = pd.read_csv(comparator_csv)
   
   # Extract comparator indices
   comparator_idx = ['MSCI World Index TR', 'Barclays Global Aggregate Bond Index TR', 'Bloomberg Commodity Index TR', 'S&P 500 Total Return Index'] 
   
   # Merge comparator indices
   for idx in comparator_idx:
      comparator_idx_df = comparator_df[['Date', idx]]
      comparator_idx_df['Trading Index'] = idx
      comparator_idx_df['Settlement Price (yuan/ton)'] = comparator_idx_df[idx]
      comparator_idx_df = comparator_idx_df[['Trading Index', 'Date', 'Settlement Price (yuan/ton)']]
      df = pd.concat([df, comparator_idx_df])
   
   display(df)
   
   if to_csv:
      df.to_csv('/Users/xuhuili/Desktop/ccm_project/web_scraping/merge_df.csv')
      
         
   
   