import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from time import sleep
from scrapy import Spider 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


class GuangdongSpider(scrapy.Spider):
    name = 'guangdong'
    start_urls = ['http://http://ets.cnemission.com/carbon/portalIndex/markethistory?Top=1/']
    
    def start_requests(self, begin_date = '2014-05-03', end_date = '2021-06-11'):
       
       
       self.Date = []
       self.Trading_index = []
       self.Open_price = []
       self.Close_price = []
       self.Highest_price = []
       self.Lowest_price = []
       self.Change = []
       self.Pct_change = []
       self.Settlement_volume = []
       self.Settlement_value = []
       
       self.driver = webdriver.Chrome('/Users/xuhuili/Desktop/ccm_project/chromedriver')
       self.driver.get('http://ets.cnemission.com/carbon/portalIndex/markethistory?Top=1')
       
       sel = Selector(text=self.driver.page_source)
       
       begin_date_key = self.driver.find_element_by_xpath('//*[@id="beginTime"]')
       end_date_key = self.driver.find_element_by_xpath('//*[@id="endTime"]')
       
       for i in range(10):
          begin_date_key.send_keys(Keys.BACK_SPACE)
          sleep(0.5)
       for i in range(10):
          end_date_key.send_keys(Keys.BACK_SPACE)
          sleep(0.5)
                    
       begin_date_key.send_keys(begin_date)
       sleep(0.5)
   
       end_date_key.send_keys(end_date)
       sleep(0.5)
   
       chaxun = self.driver.find_element_by_xpath('//*[@id="mytable1"]/tbody/tr/td/a[1]/span/span')
       chaxun.click()
       sleep(5)
       
       sel = Selector(text=self.driver.page_source)
       table = sel.xpath('//*[@id="mytable"]/tbody/tr')
       
       for i in range(1, len(table)):
          
          date = table[i].xpath('.//td[1]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          date = date[:4] + '-' + date[4:6] + '-' + date[6:]
          trading_index = table[i].xpath('.//td[2]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          open_price = table[i].xpath('.//td[3]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          close_price = table[i].xpath('.//td[4]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          highest_price = table[i].xpath('.//td[5]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          lowest_price = table[i].xpath('.//td[6]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          change = table[i].xpath('.//td[7]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          pct_change = table[i].xpath('.//td[8]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t').strip('%')
          settlement_volume = table[i].xpath('.//td[9]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          settlement_value = table[i].xpath('.//td[10]/text()').extract_first().strip('\n\t\t\t\t\t\n\t\t\t\t\t')
          
          self.Date.append(date)
          self.Trading_index.append(trading_index)
          self.Open_price.append(open_price)
          self.Close_price.append(close_price)
          self.Highest_price.append(highest_price)
          self.Lowest_price.append(lowest_price)
          self.Change.append(change)
          self.Pct_change.append(pct_change)
          self.Settlement_volume.append(settlement_volume)
          self.Settlement_value.append(settlement_value)
          
       df = pd.DataFrame( {'Date': self.Date,
              'Trading Index': self.Trading_index,
              'Open Price': self.Open_price, 
              'Settlement Price (yuan/ton)': self.Close_price,
              'Highest Price': self.Highest_price,
              'Lowest Price': self.Lowest_price,
              'Price Change': self.Change,
              'Return': self.Pct_change,
              'Settlement Volume (ton)': self.Settlement_volume,
              'Turnover (yuan)': self.Settlement_value    
       })
       
       yield scrapy.Request(df.to_csv('guangdong.csv'))

# Command line 
# scrapy crawl guangdong 