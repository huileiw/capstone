from scrapy.spiders import Spider,CrawlSpider,SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose

from scrapy.http import FormRequest, Request
#from loginform import fill_login_form

from recipe_scraper.items import Recipe

class RecipeSpider(CrawlSpider):
    name = "recipes"
    allowed_domains = ["allrecipes.com"]
    sitemap_urls = ["http://dish.allrecipes.com/faq-sitemap/"]
    start_urls = ["http://allrecipes.com/recipes/",
                    "http://allrecipes.com/recipe/"]

    rules = (
        Rule(
            LinkExtractor(allow=r'/book/show/\d+'), callback='parse_book'
        ),
        Rule(
            LinkExtractor(allow=(r'/shelf/'),deny=r'\/shelf/users'), follow = True
        ),
    )

    item_fields = {
        #'bookID': = Field()
        #'ISBN': = Field()
        #'language': = Field()
        'title': '//h1[@id="bookTitle" and @class="bookTitle"]/text()',
        'author': '(//a[@class="authorName"]/span[@itemprop="name"])[1]/text()',
        'genre': '(//a[@class="actionLinkLite bookPageGenreLink"])[1]/text()',
        'rating': '//span[@itemprop="ratingValue"]/text()',
        'no_ratings': '//span[@itemprop="ratingCount"]/text()',
        'no_reviews': '//span[@class="count"]/span[@class="value-title"]/text()',
        'no_pages': './/span[@itemprop="numberOfPages"]/text()',
        'date_publish': '//div[@class = "row" and text()[contains(., "Published")]]/text()'
        #'price': = Field()
        #'bookURL': = Field()
    }

    def start_requests(self):
        self.logger.info('start_requests')
        yield Request(self.login_url, self.parse_login)

    def parse_login(self,response):
        self.logger.info('parse_login')
        args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
        return FormRequest(url, method = method, formdata = dict(args), callback = self.start_crawl)
    
    def start_crawl(self, response) :
        self.logger.info('Logged in')
        for url in self.sitemap_urls :
            yield self.make_requests_from_url(url)

    
    def parse_book(self, response):
        #if randomSampling and random.random() > samplingProbability:
        loader = ItemLoader(Goodreads_Book(),response=response)

        loader.default_input_processor = MapCompose(unicode.strip)
        loader.default_output_processor = Join()

        for field,xpath in self.item_fields.iteritems():
            loader.add_xpath(field, xpath)
        yield loader.load_item()