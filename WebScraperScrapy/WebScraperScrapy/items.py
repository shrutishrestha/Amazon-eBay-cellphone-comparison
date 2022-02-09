import scrapy


class AmazonItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    amazon_item_number = scrapy.Field()
    item_model_number = scrapy.Field()
    manufacture_references = scrapy.Field()
    availability = scrapy.Field()
    cellular_technology = scrapy.Field()
    screen_size = scrapy.Field()
    item_weight = scrapy.Field()
    memory_storage_capacity = scrapy.Field()
    operating_system = scrapy.Field()
    url = scrapy.Field()


class MobilReview(scrapy.Item):
    amazon_item_number = scrapy.Field()
    positive_review = scrapy.Field()
    negative_review = scrapy.Field()
    unlabeled_review = scrapy.Field()


class EbayItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    mpn = scrapy.Field()
    screen_size = scrapy.Field()
    operating_system = scrapy.Field()
    storage_capacity = scrapy.Field()
    model = scrapy.Field()
