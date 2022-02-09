# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from .items import AmazonItem, MobilReview, EbayItem


class WebscraperscrapyPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('ecommerce_items.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        # for amazon
        self.create_amazon_items_table()

        # for ebay
        # self.create_ebay_items_table()

    def create_amazon_items_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS amazon_mobiles_tb""")
        self.curr.execute("""DROP TABLE IF EXISTS amazon_mobiles_reviews_tb""")

        self.curr.execute("""create table amazon_mobiles_tb (
                mobileid INTEGER PRIMARY KEY AUTOINCREMENT,
                name text,
                price float,
                item_model_number VARCHAR,
                manufacture_references VARCHAR,
                rating text,
                amazon_item_number VARCHAR,
                availability text,
                cellular_technology text,
                screen_size text,
                item_weight text,
                memory_storage_capacity text,
                operating_system text,
                url VARCHAR
                )""")

        self.curr.execute("""create table amazon_mobiles_reviews_tb(
                reviewid INTEGER PRIMARY KEY AUTOINCREMENT,
                mobileid int,
                positive_review text,
                negative_review text,
                unlabeled_review text,
                FOREIGN KEY (mobileid) REFERENCES amazon_mobiles_tb(mobileid)
                )""")

    def create_ebay_items_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS ebay_mobiles_tb""")
        self.curr.execute("""create table ebay_mobiles_tb(
            mobileid INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            price float,
            mpn VARCHAR,
            screen_size VARCHAR,
            operating_system text,
            storage_capacity text,
            model text,
            url VARCHAR
            )""")

    def process_item(self, item, spider):

        if isinstance(item, AmazonItem):
            item.setdefault('name', "N/A")
            item.setdefault('price', "N/A")
            item.setdefault('item_model_number', "N/A")
            item.setdefault("manufacture_references", "N/A")
            item.setdefault('rating', "N/A")
            item.setdefault('amazon_item_number', "N/A")
            item.setdefault('availability', "N/A")
            item.setdefault('cellular_technology', "N/A")
            item.setdefault('screen_size', "N/A")
            item.setdefault('item_weight', "N/A")
            item.setdefault('memory_storage_capacity', "N/A")
            item.setdefault('operating_system', "N/A")
            item.setdefault('url', "N/A")
            self.store_amazon_mobile_desc(item)
        elif isinstance(item, MobilReview):
            item.setdefault('amazon_item_number', "N/A")
            item.setdefault('positive_review', "N/A")
            item.setdefault('negative_review', "N/A")
            item.setdefault('unlabeled_review', "N/A")
            self.store_amazon_mobile_reviews(item)

        elif isinstance(item, EbayItem):
            item.setdefault('name', "N/A")
            item.setdefault('price', "N/A")
            item.setdefault('mpn', "N/A")
            item.setdefault('screen_size', "N/A")
            item.setdefault('operating_system', 'N/A')
            item.setdefault('storage_capacity', 'N/A')
            item.setdefault('model', "N/A")
            item.setdefault('url', "N/A")

            self.store_ebay_mobile(item)
        return item

    def store_amazon_mobile_desc(self, item):
        self.curr.execute("""insert into amazon_mobiles_tb(name, price, item_model_number, manufacture_references, rating, amazon_item_number,availability, cellular_technology, screen_size, item_weight, memory_storage_capacity, operating_system, url
    ) values (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            item['name'],
            item['price'],
            item['item_model_number'],
            item['manufacture_references'],
            item['rating'],
            item['amazon_item_number'],
            item['availability'],
            item['cellular_technology'],
            item['screen_size'],
            item['item_weight'],
            item['memory_storage_capacity'],
            item['operating_system'],
            item['url']

        ))
        self.conn.commit()

    def store_amazon_mobile_reviews(self, item):
        self.curr.execute(
            """insert into amazon_mobiles_reviews_tb(mobileid, positive_review,negative_review,unlabeled_review) values((select mobileid from amazon_mobiles_tb where amazon_item_number =?),?,?,?)""",
            (
                item['amazon_item_number'],
                item['positive_review'],
                item['negative_review'],
                item['unlabeled_review']

            ))
        self.conn.commit()

    def store_ebay_mobile(self, item):
        self.curr.execute(
            """insert into ebay_mobiles_tb(name, price, mpn, screen_size, operating_system, storage_capacity, model,url) values(?,?,?,?,?,?,?,?)""",
            (
                item['name'],
                item['price'],
                item['mpn'],
                item['screen_size'],
                item['operating_system'],
                item['storage_capacity'],
                item['model'],
                item['url']

            ))

        self.conn.commit()
