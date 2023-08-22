import scrapy

from bags_info.items import Product


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"]

    def parse(self, response):
        baseURL = 'https://www.amazon.in'
        products = response.css('div.a-section.a-spacing-small.a-spacing-top-small')
        for product in products:
            url = product.css('div.s-title-instructions-style>h2>a ::attr(href)').get()
            if url is not None:
                # name = response.follow(baseURL+url, callback=self.getDetails)
                yield scrapy.Request(url=baseURL+url,callback=self.getDetails)

        next_page = response.css('a.s-pagination-item').attrib['href']
        if next_page is not None:
            yield response.follow(baseURL+next_page,callback=self.parse)
        # page = '/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

    def getDetails(self,response):
        item = Product()
        item['product_url'] = response.request.url
        # item['product_name'] = response.css('title::text').get()
        item['product_name'] = response.css('span#productTitle::text').get().strip()
        item['product_price'] = str(response.css('span.a-price-symbol::text').get()+response.css('span.a-price-whole::text').get())
        item['product_rating'] = response.css('span.a-size-base.a-color-base::text').get().strip()
        item['product_reviews'] = response.css('span#acrCustomerReviewText::text').get().split(' ')[0]
        yield item


