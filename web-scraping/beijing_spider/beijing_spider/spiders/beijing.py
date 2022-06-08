import scrapy
import pandas as pd

class BeijingSpider(scrapy.Spider):
    name = 'beijing'
    start_urls = ['http://www.bjets.com.cn/article/jyxx//']

    def parse(self, response):
        
        table = response.xpath('//table/tr')
        
        for i in range(1, len(table)):
           date = table[i].xpath('.//td[1]/text()').extract_first()
           volume = table[i].xpath('.//td[2]/text()').extract_first()
           price = table[i].xpath('.//td[3]/text()').extract_first()
           cap = table[i].xpath('.//td[4]/text()').extract_first()
                             
           yield{'Date': date,
                 'Settlement Volume (ton)': volume,
                 'Settlement Price (yuan/ton)': price,
                 'Turnover (yuan)': cap
           }
        
        for i in range(2, 89):
           next_page_url = '?' + str(i)             
           absolute_next_page_url = response.urljoin(next_page_url)
           
           yield scrapy.Request(absolute_next_page_url, callback = self.parse)
          
           
# Command to type in the terminal
# scrapy crawl beijing -o beijing.csv    
