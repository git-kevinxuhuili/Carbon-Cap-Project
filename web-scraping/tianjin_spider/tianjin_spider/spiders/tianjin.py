import scrapy

class TianjinSpider(scrapy.Spider):
    name = 'tianjin'
    start_urls = ['https://www.chinatcx.com.cn/list/13.html?page=1']

    def parse(self, response):
       
       table = response.xpath('//*[@id="page"]/div[4]/div[2]/div/table/tr')
       
       for i in range(2, len(table)):
          
          date = table[i].xpath('.//td[1]/text()').extract_first()
          trading_index = table[i].xpath('.//td[2]/text()').extract_first()
          settlement_volume = table[i].xpath('.//td[3]/text()').extract_first()
          if settlement_volume == '-':
             settlement_volume = table[i].xpath('.//td[4]/text()').extract_first()
             if settlement_volume == '-':
                i.next()
                continue
          settlement_value = table[i].xpath('.//td[5]/text()').extract_first()
          if settlement_value == '-':
             settlement_value = table[i].xpath('.//td[6]/text()').extract_first()
          settlement_price = table[i].xpath('.//td[7]/text()').extract_first()
          if settlement_price == '-':
             settlement_price = table[i].xpath('.//td[8]/text()').extract_first()
             
          
          yield{'Date': date,
                'Trading Index': trading_index,
                'Settlement Volume (ton)': settlement_volume,
                'Turnover (yuan)': settlement_value,
                'Settlement Price (yuan/ton)': settlement_price             
          }
          
       for i in range(2, 38):
          next_page_url = 'https://www.chinatcx.com.cn/list/13.html?page=' + str(i)
          
          yield scrapy.Request(next_page_url, callback = self.parse)
          
# Command line:
# scrapy crawl tianjin -o tianjin.csv
         