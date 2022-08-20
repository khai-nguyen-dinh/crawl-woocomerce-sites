import uuid

import scrapy

from woocomerce.items import WoocomerceItem


class EveryDesignersSpider(scrapy.Spider):
    name = 'every-designers'
    allowed_domains = ['every-designers.ru']
    url = 'https://every-designers.ru'
    category_urls = ['/product-category/handbags/', '/product-category/shoes/', '/product-category/clothes/',
                     '/product-category/accessories/'
                     ]

    def start_requests(self):
        for category_url in self.category_urls:
            yield scrapy.Request(self.url + category_url + '/', callback=self.parse, dont_filter=True)

    def parse(self, response):
        product_urls = response.xpath(
            '//ul[@class="products columns-3"]/li//div[@class="image-block"]/a/@href').extract()
        print(len(product_urls))
        for url in product_urls:
            yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)
        nextpage_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if nextpage_url:
            yield scrapy.Request(nextpage_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        item = WoocomerceItem()
        item['id'] = str(uuid.uuid4())[:4]
        item['type'] = 'simple'
        item['sku'] = ''
        item['name'] = response.xpath(
            '//h1[@class="product_title entry-title"]/text()').extract_first().strip()
        item['published'] = 1
        item['is_featured'] = 1
        item['visibility_in_catalog'] = "visible"
        item['short_description'] = response.xpath(
            'string(//div[@class="woocommerce-product-details__short-description"]//ul)').extract_first().strip()
        item['description'] = response.xpath(
            'string(//div[@id="tab-description"]//ul)').extract_first().strip()
        item['date_sale_price_starts'] = ''
        item['date_sale_price_ends'] = ''
        item['tax_status'] = 'taxable'
        item['tax_class'] = ''
        item['in_stock'] = 1
        item['stock'] = ''
        item['backorders_allowed'] = 0
        item['sold_individually'] = 0
        item['weight'] = ''
        raw = response.xpath('//div[@class="woocommerce-product-details__short-description"]/ul/li//text()').extract()
        size = ''
        item['length'] = ''
        item['width'] = ''
        item['height'] = ''
        item['purchase_note'] = ''
        if raw:
            for tmp in raw:
                if 'Size' in tmp:
                    size = tmp
                    continue
                if 'Width' in tmp:
                    item['length'] = tmp.lower().replace('width:', '').replace('cm', '')
                    continue
                if 'Payment method' in tmp:
                    item['purchase_note'] = tmp.replace('Payment method:', '').replace('.', '').strip()
                    continue
        if size:
            size = size.replace('Size:', '').strip()
            size = size.lower().split('x')
            if len(size) == 3:
                item['length'] = size[0].replace('cm', '')
                item['width'] = size[1].replace('cm', '')
                item['height'] = size[2].replace('cm', '')
        item['allow_customer_reviews'] = 1

        item['regular_price'] = response.xpath(
            '//div[@class="summary entry-summary"]//span[@class="woocommerce-Price-amount amount"]/text()').extract_first()
        item['sale_price'] = ''
        categories = response.xpath('//nav[@class="woocommerce-breadcrumb"]//span/a/text()').extract()
        del categories[0]
        item['categories'] = ' > '.join(categories)
        item['tags'] = response.xpath('//span[@class="tagged_as"]/a/text()').extract()
        item['shipping_class'] = ''
        item['images'] = response.xpath('//figure[@class="woocommerce-product-gallery__wrapper"]//a/@href').extract()
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
            '//th[@class="woocommerce-product-attributes-item__label"]/text()').extract_first()
        item['attribute_1_value'] = response.xpath(
            '//td[@class="woocommerce-product-attributes-item__value"]//text()').extract_first()
        item['attribute_1_visible'] = 1
        item['attribute_1_global'] = 1
        item['attribute_2_name'] = ''
        item['attribute_2_value'] = ''
        item['attribute_2_visible'] = ''
        item['attribute_2_global'] = ''
        item['wpcom_is_markdown'] = ''
        item['download_1_name'] = ''
        item['download_1_url'] = ''
        item['download_2_name'] = ''
        item['download_2_url'] = ''
        return item
