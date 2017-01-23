import re
from scrapy.spiders import Spider,CrawlSpider,SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose

from scrapy.http import FormRequest, Request
#from loginform import fill_login_form

from recipe_scraper.items import Recipe

class RecipeSpider(SitemapSpider):
    name = "recipe_spider"
    allowed_domains = ["allrecipes.com"]
    sitemap_urls = ["http://dish.allrecipes.com/faq-sitemap/"]
    start_urls = ["http://allrecipes.com/recipes/",
                    "http://allrecipes.com/recipe/"]

    rules = (
        Rule(
            LinkExtractor(allow=r'/recipe/\d+'), callback='parse_recipe'
        ),
    """    
        Rule(
            LinkExtractor(allow=r'/recipes/'), callback = 'parse_catalog'
        ),
    """
    )

    #quotes_base_url = 'https://apps.allrecipes.com/v1/assets/hub-feed?id={}&pageNumber={}&isSponsored=true&sortType=p'
    post_nutri_url = 'https://apps.allrecipes.com/v1/recipes/{}?fields=nutrition&isMetric=false&servings={}'

    item_fields = {
        'title': '//h1[@class="recipe-summary__h1"]/text()',
        'desc': '//div[@class="submitter__description"]/text()',
        'by' : '//span[@class="submitter__name"]/text()',
        'no_made_it': '//span[@class="made-it-count ng-binding"]/text()',
        'no_reviews': '//a[@class="read--reviews"]/span[@class="review-count"]/text()',
        #'no_ratings': 
        'rating': '//span[@itemprop="aggregateRating"]/meta[@itemprop="ratingValue"]/@content',
        'servings': '//span[@ng-bind="adjustedServings"]/text()',
        #'cals': '//span[@class="calorie-count"]/text()'
        #'cals_unit': '//span[@class="calorie-count__desc"]/text()'
        #'prep_time': 
        #'cook_time': 
        #'ready_in': 
        #'no_ingre': 
        #'no_steps': 
        'ingre': '//li[@class="checkList__line"]//span[@itemprop="ingredients"]/text()',
        'steps': '//ol[@itemprop="recipeInstructions"]//span[@class="recipe-directions__list--item"]/text()'
    }

    
    def parse_recipe(self, response):
        #if randomSampling and random.random() > samplingProbability:
        item = Recipe()

        for field,xpath in self.item_fields.iteritems():
            item[field] = response.xpath(xpath).extract()

        #other items fields:
        item['no_ratings'] = re.findall(r".+?(?= )",response.xpath('//ol//h4[@class="helpful-header"]/text()').extract())[0]

        prep_time_digit = response.xpath('//time[@itemprop="prepTime"]/span[@class="prepTime__item--time"]/text()').extract()
        prep_time_unit = response.xpath('//time[@itemprop="prepTime"]/text()').extract()
        item['prep_time'] = ''.join([''.join((prep_time_digit[i], prep_time_unit[i])) for i in xrange(min(len(prep_time_digit), len(prep_time_unit)))])
        
        cook_time_digit = response.xpath('//time[@itemprop="cookTime"]/span[@class="prepTime__item--time"]/text()').extract()
        cook_time_unit = response.xpath('//time[@itemprop="cookTime"]/text()').extract()
        item['cook_time'] = ''.join([''.join((cook_time_digit[i], cook_time_unit[i])) for i in xrange(min(len(cook_time_digit), len(cook_time_unit)))])
 
        ready_in_digit = response.xpath('//time[@itemprop="totalTime"]/span[@class="prepTime__item--time"]/text()').extract()
        ready_in_unit = response.xpath('//time[@itemprop="totalTime"]/text()').extract()
        item['ready_in'] = ''.join([''.join((ready_in_digit[i], ready_in_unit[i])) for i in xrange(min(len(ready_in_digit), len(ready_in_unit)))])
 
        item['no_ingre'] = len(response.xpath('//li[@class="checkList__line"]//span[@itemprop="ingredients"]/text()').extract())

        item['no_steps'] = len(response.xpath('//ol[@itemprop="recipeInstructions"]//span[@class="recipe-directions__list--item"]/text()').extract())

        #nutrition items
        recipe_id = re.findall(r"recipe\/(\d+)\/", response.url)[0]
        servings = response.xpath('//span[@ng-bind="adjustedServings"]/text()').extract
        nutri_dict = FormRequest(self.post_nutri_url.format(recipe_id,servings), callback = self.parse_nutrition)
        for key, value in nutri_dict.iteritems():
            item[key] = value

        yield item

    def parse_nutrition(self,response):
        data = json.loads(response.body)['nutrition']
        d = dict()
        d['ntri_cals'] = data['calories']['amount'].strip() + ' ' + data['calories']['unit'].strip()
        d['ntri_cals_fat']  = data['caloriesFromFat']['amount'].strip() + ' ' + data['caloriesFromFat']['unit'].strip()
        d['ntri_tt_fat']  = data['fat']['amount'].strip() + ' ' + data['fat']['unit'].strip()
        d['ntri_sat_fat']  = data['saturatedFat']['amount'].strip() + ' ' + data['saturatedFat']['unit'].strip()
        d['ntri_cholstl'] = data['cholesterol']['amount'].strip() + ' ' + data['cholesterol']['unit'].strip()
        d['ntri_sodium']  = data['sodium']['amount'].strip() + ' ' + data['sodium']['unit'].strip()
        d['ntri_carbo']  = data['carbohydrates']['amount'].strip() + ' ' + data['carbohydrates']['unit'].strip()
        d['ntri_sugr']  = data['sugars']['amount'].strip() + ' ' + data['sugars']['unit'].strip()
        d['ntri_fibr']  = data['fiber']['amount'].strip() + ' ' + data['fiber']['unit'].strip()
        d['ntri_prtein'] = data['protein']['amount'].strip() + ' ' + data['protein']['unit'].strip()
        d['ntri_vA']  = data['vitaminA']['amount'].strip() + ' ' + data['vitaminA']['unit'].strip()
        d['ntri_vC'] = data['vitaminC']['amount'].strip() + ' ' + data['vitaminC']['unit'].strip()
        d['ntri_calc']  = data['calcium']['amount'].strip() + ' ' + data['calcium']['unit'].strip()
        d['ntri_iron']  = data['iron']['amount'].strip() + ' ' + data['iron']['unit'].strip()
        d['ntri_potasm'] = data['potassium']['amount'].strip() + ' ' + data['potassium']['unit'].strip()
        d['ntri_thiamin']  = data['thiamin']['amount'].strip() + ' ' + data['thiamin']['unit'].strip()
        d['ntri_niacin']  = data['niacin']['amount'].strip() + ' ' + data['niacin']['unit'].strip()
        d['ntri_vB6']  = data['vitaminB6']['amount'].strip() + ' ' + data['vitaminB6']['unit'].strip()
        d['ntri_magnsm']  = data['magnesium']['amount'].strip() + ' ' + data['magnesium']['unit'].strip()
        d['ntri_folate']  = data['folate']['amount'].strip() + ' ' + data['folate']['unit'].strip()
        return d

"""
    def parse_catalog(self, response):
        if not response.Selector.xpath("//button[@class='btns-one-small']"):
            catalog_id = re.findall(r"recipes\/(\d+)\/", response.url)[0]
            link = response.Selector.xpath("//button[@class='btns-one-small ng-hide']/@href").strip()
            next_page = int(re.findall(r"page=(\d+)", link)[0]) + 1
            yield scrapy.request(self.quotes_base_url.format( catalog_id , next_page))
        else:
            yield
"""
