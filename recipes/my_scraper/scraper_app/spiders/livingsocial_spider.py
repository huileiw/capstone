from scrapy.spiders import Spider,CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose

from scrapy.http import FormRequest
from loginform import fill_login_form

from scraper_app.items import LivingSocialDeal

class LivingSocialSpider(CrawlSpider):
    name = "livingsocial"
    allowed_domains = ["livingsocial.com"]
    start_urls = ["https://www.livingsocial.com/things-to-do/arlington-alexandria",
                "https://www.livingsocial.com/products/us"]
    login_url = ["https://login.livingsocial.com/?return_to=https://login.livingsocial.com/"]
    login_user = "kukuhelen@gmail.com"
    login_pass = "058976c03"

    rules = (
        Rule(
            LinkExtractor(allow='/product/\d+'), follow = True
        ),
    )

    deals_list_xpath = '//li[@dealid]'
    item_fields = {
        'title': './/span[@itemscope]/meta[@itemprop="name"]/@content',
        'link': './/a/@href',
        'location': './/a/div[@class="deal-details"]/p[@class="location"]/text()',
        'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
        'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
        'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'
    }

    def start_request(self):
        yield scrapy.Request(self.login_url, self.parse_login)

    def parse_login(self,response):
        args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
        return FormRequest(url, method = method, formdata = dict(args), callback = self.start_crawl)
    
    def start_crawl(self, response) :
        for url in self.start_urls :
            yield self.make_requests_from_url(url)
    
    def parse(self, response):
        selector = Selector(response)
        for deal in selector.xpath(self.deals_list_xpath):
            loader = ItemLoader(LivingSocialDeal(),selector=deal)

            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field,xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()