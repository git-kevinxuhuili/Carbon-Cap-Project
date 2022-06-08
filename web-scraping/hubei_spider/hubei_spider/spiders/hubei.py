import scrapy


class HubeiSpider(scrapy.Spider):
    name = 'hubei'
    start_urls = ['http://www.hbets.cn/list/13.html']

    def parse(self, response):
        
        table = response.xpath('/html/body/div[5]/div/div/div[2]/div/div/ul')
        
        for i in range(1, len(table)):
           
           index = table[i].xpath('.//li[1]/text()').extract_first()
           date = table[i].xpath('.//li[2]/text()').extract_first()
           newest_price = table[i].xpath('.//li[3]/text()').extract_first()
           # pct_change = table[i].xpath('.//li[4]/text()').extract_first().strip('%')
           highest_price = table[i].xpath('.//li[5]/text()').extract_first()
           lowest_price = table[i].xpath('.//li[6]/text()').extract_first()
           settlement_volume = table[i].xpath('.//li[7]/text()').extract_first()
           settlement_value = table[i].xpath('.//li[8]/text()').extract_first()
           
           yield {'Trading Index': index,
                  'Date': date,
                  'Settlement Price (yuan/ton)': newest_price,
                  # 'Return (%)': pct_change, 
                  'Highest Price': highest_price, 
                  'Lowest Price': lowest_price, 
                  'Settlement Volume (ton)': settlement_volume,
                  'Turnover (yuan)': settlement_value}
               
        for i in range(2, 51):
           next_page_url = '?page=' + str(i)
           absolute_next_page_url = response.urljoin(next_page_url)
           
           yield scrapy.Request(absolute_next_page_url, callback = self.parse)

# Command line
# scrapy crawl hubei -o hubei.csv