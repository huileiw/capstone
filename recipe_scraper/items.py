# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Recipe(Item):
    #bookID = Field()
    title = Field()
    recipe_id = Field()
    desc = Field()
    by = Field()
    no_made_it = Field()
    no_reviews = Field()
    no_ratings = Field()
    rating = Field()
    #servings = Field()
    prep_time = Field()
    cook_time = Field()
    ready_in = Field()
    no_ingre = Field()
    no_steps = Field()
    ingre = Field()
    steps = Field()
    Cat1 = Field()
    Cat2 = Field()
    Cat3 = Field()
    Cat4 = Field()
    """
    ntri_cals = Field()
    ntri_cals_fat  = Field()
    ntri_tt_fat  = Field()
    ntri_sat_fat  = Field()
    ntri_cholstl  = Field()
    ntri_sodium  = Field()
    ntri_carbo  = Field()
    ntri_sugr  = Field()
    ntri_fibr  = Field()
    ntri_prtein = Field()
    ntri_vA  = Field()
    ntri_vC = Field()
    ntri_calc  = Field()
    ntri_iron  = Field()
    ntri_potasm = Field()
    ntri_thiamin  = Field()
    ntri_niacin  = Field()
    ntri_vB6  = Field()
    ntri_magnsm  = Field()
    ntri_folate  = Field()
    """

    
