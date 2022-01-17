# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker, aliased
from woninglabel.models import ItemData, db_connect, create_tables
from woninglabel.items import WoninglabelItem
import datetime
import woninglabel.settings


class WoninglabelPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def close_spider(self, spider):
        
        session = self.Session()
        session.commit()
        
        session.close()

    def process_item(self, item, spider):
        """

        This method is called for every item pipeline component.

        """
        session = self.Session()
        property = ItemData(**item)

        try:
            
            instance = session.query(ItemData).filter_by(
                ObjectId=item["ObjectId"], Bedrijf=item['Bedrijf']
            ).first()
            
            if not instance:

                session.add(property)
                session.commit()
            else:
                pass
                # session.query(ItemData).filter_by(
                #     ItemNumber=item["ItemNumber"]
                # ).update( dict(
                #                         
                #     HP=item["HP"],
                #     RPM=item["RPM"],
                #     Voltage=item["Voltage"],
                #     Frame=item["Frame"],
                #     Enclosure=item["Enclosure"],
                #     Bearing=item["Bearing"],
                #     Condition=item["Condition"],
                #     Quantity=item["Quantity"],
                #     Problem=item["Problem"],
                #     ItemURL=item["ItemURL"],
                #     ImagesAvailable=item["ImagesAvailable"],
                #     ImageURLs=item["ImageURLs"]
                #     
                # ) )
                # session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()
    
        return item


