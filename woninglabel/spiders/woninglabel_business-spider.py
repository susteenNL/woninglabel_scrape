# -*- coding: utf-8 -*-

import scrapy
from woninglabel.items import WoninglabelItem
from scrapy.loader import ItemLoader
import csv
from datetime import datetime
import json
import logging


class WoninglabelSpider(scrapy.Spider):

    name = 'woninglabel_business'
    start_urls = ['https://woninglabel.nl/vergelijk']
    addresses_file = 'AddressesBusiness.csv'
    debug = False

    def parse(self, response):
        with open(self.addresses_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                postcode = row['Postcode']
                house_number = row['Huisnr']
                row['Type woning'] = 'Business'

                # DEBUG
                # if self.debug:
                #     postcode = '9403AD'
                #     house_number = '69'

                yield scrapy.Request(
                    url=f'https://woninglabel.nl/api/v1/public/bag/business/{postcode}/{house_number}',
                    callback=self.perform_search,
                    cb_kwargs={
                        'row': row,
                    }
                )

                # DEBUG
                if self.debug:
                    break

    def perform_search(self, response, row):
        data = json.loads(response.text)
        if 'result' in data:
            if 'areaCode' in data['result']:
                area_code = data['result']['areaCode']
                payload = {
                    "filters":
                        { 
                            "area": area_code, "buildingType": "Business", "buildingTypeCategory": "business",
                            "fullAdvisors": False, "methodology":"basic", "priceMax": 1495, 
                            "targetZipCode": row['Postcode']
                        },
                    "orderBy": "reviewAverage",
                    "page": 1,
                }
                body = json.dumps(payload)
                yield scrapy.FormRequest(
                    method='POST',
                    url='https://woninglabel.nl/api/v1/public/search',
                    callback=self.parse_search,
                    body=body,
                    headers={
                        'Content-type': 'text/plain;charset=UTF-8',
                    },
                    cb_kwargs={
                        'row': row,
                        'area_code': area_code,
                        'page': 1,
                    }
                )

    def parse_search(self, response, row, area_code, page):

        data = json.loads(response.text)
        if data['nextPage']:
            page += 1
            payload = {
                "filters":
                    { 
                        "area": area_code, "buildingType": "Business", "buildingTypeCategory": "business",
                        "fullAdvisors": False, "methodology":"basic", "priceMax": 1495, 
                        "targetZipCode": row['Postcode']
                    },
                "orderBy": "reviewAverage", 
                "page": page,
            }
            body = json.dumps(payload)
            yield scrapy.FormRequest(
                method='POST',
                url='https://woninglabel.nl/api/v1/public/search',
                callback=self.parse_search,
                body=body,
                headers={
                    'Content-type': 'text/plain;charset=UTF-8',
                },
                cb_kwargs={
                    'row': row,
                    'area_code': area_code,
                    'page': page,
                }
            )

        for record in data['result']:
            l = ItemLoader(item=WoninglabelItem())
            l.add_value('postcode', row['Postcode'])
            l.add_value('huisnr', row['Huisnr'])
            l.add_value('type', row['Type woning'])
            l.add_value('scrape_date', datetime.strftime(datetime.now(), '%Y-%m-%d'))
            l.add_value('bedrijf', record['advisor']['companyName'])
            l.add_value('beoordeling', record['advisor']['reviewAverage'])
            l.add_value('beoordeling_aantal', record['advisor']['reviewTotalCount'])
            l.add_value('levertijd', record['advisor']['deliveryTime'])
            l.add_value('prijs', record['price'])

            item = l.load_item()
            yield item
