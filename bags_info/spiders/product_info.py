import scrapy

from bags_info.items import Info


class ProductInfoSpider(scrapy.Spider):
    name = "product_info"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"]

    def parse(self, response):
        baseURL = 'https://www.amazon.in'
        products = response.css('div.a-section.a-spacing-small.a-spacing-top-small')
        for product in products:
            url = product.css('div.s-title-instructions-style>h2>a ::attr(href)').get()
            if url is not None:
                yield scrapy.Request(url=baseURL+url,callback=self.getDetails)

        next_page = response.css('a.s-pagination-item').attrib['href']
        if next_page is not None:
            yield response.follow(baseURL+next_page,callback=self.parse)
        # page = '/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

    def getDetails(self,response):
        item = Info()
        url = response.request.url
        ind = url.index('/dp/')
        item['asin'] = url[ind+4:ind+14]
        item['des'] = response.css('div#productDescription>p>span::text').get()
        yield item
