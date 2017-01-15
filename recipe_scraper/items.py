# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Recipe(Item):
    #bookID = Field()
    title = Field()
    desc = Field()
    made_it = Field()
    reviews = Field()
    servings = Field()
    cals = Field()
    prep_time = Field()
    cook_time = Field()
    ready_in = Field()
    no_ingre = Field()
    no_steps = Field()
    ingre = Field()
    steps = Field()
    nutrients = Field()
    #type_meal = 
    #type_ingre = 
    #type_diet = 
    #type_season = 
    #type_dish = 
    #type_cooking = 
    #type_world = 
    #type_special = 
    
