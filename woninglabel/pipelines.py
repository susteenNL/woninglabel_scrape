# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker, aliased
from models import Categories, db_connect, create_tables
from categories.items import CategoriesItem
import datetime
import settings


class CategoriesPipeline(object):
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
        
        Parent = aliased(Categories)
        # record = Categories(**item)

        try:
            
            if item["ParentName"]:
                category_id = session.query( Categories, Parent ).join(
                        (Parent, Categories.ParentID==Parent.ID)
                    ).filter(
                    Categories.Name == item["Name"],
                    Parent.Name==item["ParentName"]).first()
            else:
                category_id = session.query( Categories ).filter(
                    Categories.Name == item["Name"],
                    Categories.ParentID == 0).first()
            
            if not category_id:
            
                parent_id = session.query( Categories ).filter(
                    Categories.Name == item["ParentName"]).first()
                
                # instance = session.query(Categories).filter_by(
                #     Name=item["Name"]
                # ).first()
                
                if not parent_id:
                    parent_id = 0
                else:
                    parent_id = parent_id.ID
                
                category = Categories( Name = item["Name"], ParentID = parent_id )
                    
                session.add(category)
                session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()
    
        return item


