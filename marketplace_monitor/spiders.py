import scrapy
from marketplace_monitor.utils import save_product


class WildberriesSpider(scrapy.Spider):
    name = "wildberries_spider"
    start_urls = [
        'https://www.wildberries.ru/catalog/0/search.aspx?sort=priceup&q=колье',
        'https://www.wildberries.ru/catalog/0/search.aspx?sort=priceup&q=дуршлаг',
        'https://www.wildberries.ru/catalog/0/search.aspx?sort=priceup&q=красные+носки',
        'https://www.wildberries.ru/catalog/0/search.aspx?sort=priceup&q=леска+для+спиннинга',
    ]

    def parse(self, response):
        for product in response.css('div.product-card'):
            data = {
                'title': product.css('span.goods-name::text').get(),
                'price': product.css('span.price-current::text').get(),
                'link': product.css('a.ref_goods_n_p::attr(href)').get(),
            }
            save_product(data)


class OzonSpider(scrapy.Spider):
    name = "ozon_spider"
    start_urls = [
        'https://www.ozon.ru/search/?text=телефон',
    ]

    def parse(self, response):
        for product in response.css('div.c2qv4 div a'):
            title = product.css('span.j4::text').get()
            price = product.css('span.x5::text').re_first(r'\d+')
            link = product.css('::attr(href)').get()

            if title and price and link:
                data = {
                    'title': title,
                    'price': price,
                    'link': response.urljoin(link),
                }
                save_product(data)

        next_page = response.css('a[aria-label="Следующая страница"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
