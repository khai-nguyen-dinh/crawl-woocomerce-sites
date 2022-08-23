# Scrapy settings for woocomerce project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'woocomerce'

SPIDER_MODULES = ['woocomerce.spiders']
NEWSPIDER_MODULE = 'woocomerce.spiders'
# CLOSESPIDER_PAGECOUNT = 15
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'woocomerce (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'woocomerce.middlewares.WoocomerceSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'woocomerce.middlewares.WoocomerceDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'woocomerce.pipelines.ImagePipeline': 1,
    'woocomerce.pipelines.UpdateLinkPipeline': 2,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    'woocomerce.pipelines.WoocomercePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    # 'woocomerce.middlewares.proxyline_proxy.ProxyLineMiddleware': 100,
}
# PLAYWRIGHT_ABORT_REQUEST = lambda req: req.resource_type == "image"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
FEED_EXPORT_FIELDS = ['id', 'type', 'sku', 'name', 'published', 'is_featured', 'visibility_in_catalog',
                      'short_description', 'description', 'date_sale_price_starts', 'date_sale_price_ends',
                      'tax_status', 'tax_class', 'in_stock', 'stock', 'backorders_allowed', 'sold_individually',
                      'weight', 'length', 'width', 'height', 'allow_customer_reviews', 'purchase_note', 'sale_price',
                      'regular_price', 'categories', 'tags', 'shipping_class', 'images', 'download_limit',
                      'download_expiry_days', 'parent', 'grouped_products', 'upsells', 'cross_sells', 'external_url',
                      'button_text', 'position', 'attribute_1_name', 'attribute_1_value', 'attribute_1_visible',
                      'attribute_1_global', 'attribute_2_name', 'attribute_2_value', 'attribute_2_visible',
                      'attribute_2_global', 'wpcom_is_markdown', 'download_1_name', 'download_1_url', 'download_2_name',
                      'download_2_url']
IMAGES_STORE = 'data'
IMAGES_URLS_FIELD = 'all_image'
IMAGES_RESULT_FIELD = 'downloaded_images'
PROXY_IGNORE_HOST = []
#
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
