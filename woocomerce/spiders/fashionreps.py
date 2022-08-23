import uuid

import scrapy

from woocomerce.items import WoocomerceItem


class FashionrepsSpider(scrapy.Spider):
    name = 'fashionreps'
    allowed_domains = ['www.fashionreps.me']
    url = 'https://www.fashionreps.me'

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.xpath(
            '//div[@class="dropdown-menu level1"]/div/div/div/div/ul/li[@class="parent dropdown-submenu "]/a[@class="dropdown-toggle"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        urls = response.xpath('//h6[@class="name"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)
        next_page = response.xpath('//ul[@class="pagination"]/li/a[contains(.,">")]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_list, dont_filter=True)

    def parse_detail(self, response):
        item = WoocomerceItem()
        item['id'] = str(uuid.uuid4())[:4]
        item['type'] = 'simple'
        item['sku'] = ''
        item['name'] = response.xpath(
            '//h1[@class="heading-left"]/text()').extract_first('').strip()
        item['published'] = 1
        item['is_featured'] = 1
        item['visibility_in_catalog'] = "visible"
        item['short_description'] = ''
        item['description'] = [self.url + path for path in
                               response.xpath('//div[@class="tab-content"]/div/p/img/@src').extract()]

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

        item['regular_price'] = response.xpath('//span[@class="price-old"]/text()').extract_first('').strip().replace(
            '$', '')
        if item['regular_price']:
            item['sale_price'] = response.xpath('//span[@class="price-new"]/text()').extract_first('').strip().replace(
                '$', '')
        else:
            item['sale_price'] = ''
            item['regular_price'] = response.xpath('//span[@class="price-new"]/text()').extract_first(
                '').strip().replace('$', '')

        categories = response.xpath('//div[@class="breadcrumb"]//li/a/text()').extract()
        del categories[-1]
        item['categories'] = ' > '.join(categories)
        item['tags'] = ''
        item['shipping_class'] = ''
        item['images'] = response.xpath('//div[@class="item clearfix"]//img/@src').extract()
        item['download_limit'] = ''
        item['download_expiry_days'] = ''
        item['parent'] = categories[0]
        item['grouped_products'] = ''
        item['upsells'] = ''
        item['cross_sells'] = ''
        item['external_url'] = ''
        item['button_text'] = ''
        item['position'] = 0
        item['attribute_1_name'] = response.xpath(
            '(//div[@id="product"]/div[@class="form-group required"]/label/text())[1]').extract_first('').strip()
        item['attribute_1_value'] = response.xpath(
            '(//div[@id="product"]/div[@class="form-group required"]/select)[1]/option/text()').extract()
        if item['attribute_1_value']:
            del item['attribute_1_value'][0]
            item['attribute_1_value'] = [e.strip() for e in item['attribute_1_value']]
        item['attribute_1_visible'] = 1
        item['attribute_1_global'] = 1
        item['attribute_2_name'] = response.xpath(
            '(//div[@id="product"]/div[@class="form-group required"]/label/text())[2]').extract_first('').strip()
        item['attribute_2_value'] = response.xpath(
            '(//div[@id="product"]/div[@class="form-group required"]/select)[2]/option/text()').extract()
        if item['attribute_2_value']:
            del item['attribute_2_value'][0]
            item['attribute_2_value'] = [e.strip() for e in item['attribute_2_value']]
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
        item['all_image'] = item['images'] + item['description']
        return item
