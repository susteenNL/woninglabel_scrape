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
    
    object_id = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    postcode = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    huisnr = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    type = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    scrape_date = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    bedrijf = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    beoordeling = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    beoordeling_aantal = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    levertijd = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    prijs = scrapy.Field( input_processor=MapCompose(clear), output_processor=TakeFirst() )
    
    pass