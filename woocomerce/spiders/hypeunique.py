import uuid

import scrapy

from woocomerce.items import WoocomerceItem


class HypeuniqueSpider(scrapy.Spider):
    name = 'hypeunique'
    allowed_domains = ['hypeunique.is']
    url = 'https://hypeunique.is/new-releases/'

    def start_requests(self):
        yield scrapy.Request(self.url, meta={"playwright": True}, callback=self.parse, dont_filter=True)

    # def parse(self, response):
    #     urls = response.xpath('//ul[@class="main-menu mega-menu show-arrow sub-ready"]/li/a/@href').extract()
    #     for url in urls:
    #         yield scrapy.Request(url, meta={"playwright": True}, callback=self.parse_list)

    def parse(self, response):
        urls = response.xpath('//div[@class="archive-products"]/ul/li//div[@class="product-content"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, meta={"playwright": True}, callback=self.parse_detail)
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, meta={"playwright": True}, callback=self.parse)

    def parse_detail(self, response):
        item = WoocomerceItem()
        item['id'] = str(uuid.uuid4())[:4]
        item['type'] = 'simple'
        item['sku'] = response.xpath('//span[@class="sku"]/text()').extract_first()
        item['name'] = response.xpath(
            '//h2[@class="product_title entry-title show-product-nav"]/text()').extract_first().strip()
        item['published'] = 1
        item['is_featured'] = 1
        item['visibility_in_catalog'] = "visible"
        item['short_description'] = response.xpath(
            'string(//div[@class="description woocommerce-product-details__short-description"])').extract_first().strip()
        item['description'] = response.xpath(
            'string(//div[@class="description woocommerce-product-details__short-description"])').extract_first().strip()
        item['date_sale_price_starts'] = ''
        item['date_sale_price_ends'] = ''
        item['tax_status'] = 'taxable'
        item['tax_class'] = ''
        item['in_stock'] = 1
        item['stock'] = ''
        item['backorders_allowed'] = 0
        item['sold_individually'] = 0
        item['weight'] = ''
        item['length'] = ''
        item['width'] = ''
        item['height'] = ''
        item['allow_customer_reviews'] = 1
        item['purchase_note'] = ''

        item['regular_price'] = response.xpath('//p[@class="price"]//del[@aria-hidden]//bdi/text()').extract()
        if item['regular_price']:
            item['sale_price'] = response.xpath('//p[@class="price"]//ins//bdi/text()').extract()
        else:
            item['sale_price'] = ''
            item['regular_price'] = response.xpath('//p[@class="price"]//bdi/text()').extract()
        categories = response.xpath('string(//span[@class="yoast-breadcrumbs"])').extract_first().strip()
        categories = categories.replace(r'»', '>')
        categories = [i.strip() for i in categories.split('>')[1:-1]]
        item['categories'] = ' > '.join(categories)
        item['tags'] = response.xpath('//span[@class="tagged_as"]//a/text()').extract()
        item['shipping_class'] = ''
        try:
            thumbnail = list(
                set(response.xpath('//div[@class="owl-stage"]//div[@class="img-thumbnail"]//img/@src').extract()))
        except Exception as e:
            print(e)
            thumbnail = []
        images = response.xpath(
            '//div[@class="tab-content resp-tab-content resp-tab-content-active"]//p/img/@src').extract()
        images = images + thumbnail
        tmp = []
        for image in images:
            if 'porto_placeholders' not in image:
                tmp.append(image)
        item['images'] = tmp
        item['download_limit'] = ''
        item['download_expiry_days'] = ''
        item['parent'] = 'New Release'
        item['grouped_products'] = ''
        item['upsells'] = ''
        item['cross_sells'] = ''
        item['external_url'] = ''
        item['button_text'] = ''
        item['position'] = 0
        item['attribute_1_name'] = response.xpath(
            '(//th[@class="woocommerce-product-attributes-item__label"]/text())[1]').extract_first()
        item['attribute_1_value'] = response.xpath(
            '(//td[@class="woocommerce-product-attributes-item__value"]/p/text())[1]').extract_first()
        item['attribute_1_visible'] = 1
        item['attribute_1_global'] = 1
        item['attribute_2_name'] = response.xpath(
            '(//th[@class="woocommerce-product-attributes-item__label"]/text())[2]').extract_first()
        item['attribute_2_value'] = response.xpath(
            '(//td[@class="woocommerce-product-attributes-item__value"]/p/text())[2]').extract_first()
        item['attribute_2_visible'] = ''
        item['attribute_2_global'] = ''
        if item['attribute_2_name']:
            item['attribute_2_visible'] = 1
            item['attribute_2_global'] = 1
        item['wpcom_is_markdown'] = ''
        item['download_1_name'] = ''
        item['download_1_url'] = ''
        item['download_2_name'] = ''
        item['download_2_url'] = ''
        return item
