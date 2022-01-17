# -*- coding: utf-8 -*-

import scrapy
from woninglabel.items import WoninglabelItem
from scrapy.loader import ItemLoader
import csv
from datetime import datetime
import json
import logging


class WoninglabelSpider(scrapy.Spider):

    name = 'woninglabel_private'
    start_urls = ['https://woninglabel.nl/vergelijk']
    addresses_file = 'AddressesPrivate.csv'
    debug = False
    building_types = {
        'Appartement': 'Apartment',
        'Rij/Tussen': 'TerracedHouse',
        'Hoek/2-onder-1-kap': 'SemiDetachedHouse',
        'Vrijstaand': 'DetachedHouse',
    }

    def parse(self, response):
        with open(self.addresses_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                postcode = row['Postcode']
                house_number = row['Huisnr']

                # DEBUG
                if self.debug:
                    postcode = '1077JR'
                    house_number = '126'
                    row['Type woning'] = 'Appartement'

                row['Building type'] = self.building_types[row['Type woning']]
                yield scrapy.Request(
                    url=f'https://woninglabel.nl/api/v1/public/bag/private/{postcode}/{house_number}',
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
                            "area": area_code, "buildingType": row['Building type'], "buildingTypeCategory": "private",
                            "fullAdvisors": False, "methodology":"basic", "priceMax":1495, 
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
                        "area": area_code, "buildingType": row['Building type'], "buildingTypeCategory": "private",
                        "fullAdvisors": False, "methodology":"basic", "priceMax":1495, 
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
            l.add_value('ObjectId', row['nr'])
            l.add_value('Postcode', row['Postcode'])
            l.add_value('Huisnr', row['Huisnr'])
            l.add_value('Type', row['Type woning'])
            l.add_value('ScrapeDate', datetime.strftime(datetime.now(), '%Y-%m-%d'))
            l.add_value('Bedrijf', record['advisor']['companyName'])
            l.add_value('Beoordeling', record['advisor']['reviewAverage'])
            l.add_value('BeoordelingAantal', record['advisor']['reviewTotalCount'])
            l.add_value('Levertijd', record['advisor']['deliveryTime'])
            l.add_value('Prijs', record['price'])

            item = l.load_item()
            yield item
