# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
import re


def clear(value):
    if value is None:
        value = ""
    if isinstance( value, str ):
        value = value.strip()                
    return value

def update_description(value):
    value = value.replace('<br>', '\n')
    return value

def clear_abstract(value):
    value = re.sub(r'.+?\*\*Abstract:\*\*', '**Abstract:**', value, flags=re.DOTALL)
    return value

def remove_html_tags(value):
    if value is None:
        value = ""
    if isinstance( value, str ):
        value = re.sub( r'<[^>]+>', "", value )
    return value

class WoninglabelItem(scrapy.Item):
    
    ObjectId = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    Postcode = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    Huisnr = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    Type = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    ScrapeDate = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    Bedrijf = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    Beoordeling = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    BeoordelingAantal = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    Levertijd = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    Prijs = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    
    pass