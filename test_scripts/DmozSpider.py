import scrapy

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class DmozSpider(scrapy.Spider):
    name = "yahoo"
    allowed_domains = ["yahoo.com"]
    start_urls = [
        "https://login.yahoo.com"
    ]

    found_content = []

    def parse(self, response):
        
        print str(response)
        
        ifield = response.xpath('//input[contains(@id,"login-username")]')
        
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@id="login-username-form"]',
            formdata={
                'username': 'john@yahoo.com'
            },
            callback=self.after_login
        )
        
        
        """
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
        """
        
        
    def after_login(self, response):
        print response