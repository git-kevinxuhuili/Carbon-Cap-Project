import scrapy

class ShenzhenSpider(scrapy.Spider):
    name = 'shenzhen'
    start_urls = ['http://cerx.cn/dailynewsCN/index_1.htm']

    def parse(self, response):
        
        table = response.xpath('//*[@id="main"]/div[2]/div[1]/div[3]/div/table/tr')
        
        for i in range(1, len(table)):
           
           date = table[i].xpath('.//td[1]/text()').extract_first()
           trading_index = table[i].xpath('.//td[2]/text()').extract_first()
           open_price = table[i].xpath('.//td[3]/text()').extract_first()
           highest_price = table[i].xpath('.//td[4]/text()').extract_first()
           lowest_price = table[i].xpath('.//td[5]/text()').extract_first()
           settlement_price = table[i].xpath('.//td[6]/text()').extract_first()
           close_price = table[i].xpath('.//td[7]/text()').extract_first()
           settlement_volume = table[i].xpath('.//td[8]/text()').extract_first()
           settlement_value = table[i].xpath('.//td[9]/text()').extract_first()
           
           yield{'Date': date, 
                 'Trading Index': trading_index,
                 'Open Price': open_price,
                 'Highest Price': highest_price,
                 'Lowest Price': lowest_price,
                 'Settlement Price (yuan/ton)': close_price, # settlement_price
                 'Close Price': close_price,
                 'Settlement Volume (ton)': settlement_volume,
                 'Turnover (yuan)': settlement_value  
           }
           
        for i in range(2, 383):
           next_page_url = 'http://cerx.cn/dailynewsCN/index_' + str(i) + '.htm'
         
           yield scrapy.Request(next_page_url, callback = self.parse)  
         
# Command line 
# scrapy crawl shenzhen -o shenzhen.csv   