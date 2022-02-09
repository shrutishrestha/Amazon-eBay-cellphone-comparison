import scrapy
from ..items import AmazonItem,MobilReview, EbayItem
import re

class AmazonScraper(scrapy.Spider):
    name = 'amazon'
    page_number = 1
    start_urls = [
        'https://www.amazon.co.uk/s?k=samsung+galaxy&s=price-desc-rank&qid=1604130055&ref=sr_st_price-desc-rank'
    ]


    def parse(self, response, **kwargs):
        data = response.css("h2.a-size-mini")
        for i in data:
            product_link = i.css('.a-size-mini a::attr(href)').extract_first()
            yield response.follow(product_link, self.product_detail)
        next_page = 'https://www.amazon.co.uk/s?k=samsung+galaxy&s=price-desc-rank&page='+str(AmazonScraper.page_number)+'&qid=1604130062&ref=sr_pg_2'
        if AmazonScraper.page_number <= 5 :
            AmazonScraper.page_number += 1
            yield response.follow(next_page, callback=self.parse)


    def product_detail(self, response):
        mobile_criteria = 0
        productname = response.css('span#productTitle::text').extract()
        strProduct = ' '.join([str(elem) for elem in productname])
        url = response.url
        price = response.css('span.priceBlockBuyingPriceString::text').extract_first()
        if not price:
            data = response.css('table.comparison_table')
            price = data.css('td>span.a-color-price::text').extract_first()
        rating = response.css('span#acrPopover::attr(title)').extract_first()
        if not rating:
            rating = response.css('.comparison_baseitem_column span.a-icon-alt::text').extract_first()
        availability = response.css('div#availability>span::text').extract_first()
        item = AmazonItem()

        field_name_from_specs = response.css('td.a-span3 span.a-size-base::text').extract()
        field_name_from_comparison = response.css('.comparison_table_first_col span.a-color-base::text').extract()[3:]
        field_name = field_name_from_specs + field_name_from_comparison

        field_value_from_specs = response.css('td.a-span9 span.a-size-base::text').extract()
        field_value_from_comparison = response.css('.comparison_baseitem_column span.a-color-base::text').extract()
        field_value = field_value_from_specs + field_value_from_comparison

        item['url'] = url
        item['amazon_item_number'] = url.split("/")[5]
        item['name'] = strProduct.strip().replace('\n', '')
        if price and price!="":
            price = re.sub(r'[A-Za-z£$]+', '', price, re.I).strip()
            item['price'] = float(price.replace(",",""))
        if rating:
            item['rating'] = rating
        if availability:
            item['availability']= availability

        product_details = response.css("ul.detail-bullet-list>li>span>span::text").extract()
        for item_index in range(len(product_details)):
            if product_details[item_index].find("model number") != -1:
                item_model_number = product_details[item_index+1]
                item["item_model_number"] = item_model_number
                mobile_criteria += 1
            if product_details[item_index].find("Manufacturer reference") !=-1:
                manufacture_references = product_details[item_index+1]
                item['manufacture_references'] = manufacture_references

        for i in range(len(field_name)):
            if field_name[i] not in item.keys():

                if (field_name[i] == "Screen Size" or field_name[i] == 'Display Size'):
                    item['screen_size'] = field_value[i]

                elif (field_name[i] == "Operating System"):
                    item['operating_system'] = field_value[i]
                    mobile_criteria+=1

                elif (field_name[i] == "Memory Storage Capacity"):
                    item['memory_storage_capacity'] = field_value[i]
                    mobile_criteria+=1

                elif (field_name[i] == "Cellular Technology"):
                    item['cellular_technology'] = field_value[i]

                elif (field_name[i] == "Item Weight"):
                    item['item_weight'] = field_value[i]


        if mobile_criteria > 0 and item['name']:
            yield item

            #for reviews
            reviews_url = response.css("a.a-link-emphasis::attr(href)").extract_first()
            if reviews_url:
                yield response.follow(reviews_url, self.get_reviews)


    def get_reviews(self,response):
        review_url = response.css('span.a-declarative a.see-all::attr(href)').extract()
        if review_url:
            positive_review_url = response.css('span.a-declarative a.see-all::attr(href)').extract()[0]
            negative_review_url = response.css('span.a-declarative a.see-all::attr(href)').extract()[1]

            yield response.follow(positive_review_url, self.positive_reviews)
            yield response.follow(negative_review_url, self.negative_reviews)
        else:
            url = response.url
            amazon_item_number = url.split("/")[5]
            review_item = MobilReview()
            review_list = response.css('span.review-text-content span::text').extract()
            for review in review_list:
                review_item["unlabeled_review"] = review
                review_item["amazon_item_number"] = amazon_item_number
                yield review_item


    def positive_reviews(self, response):
        url = response.url
        amazon_item_number = url.split("/")[5]
        review_item = MobilReview()
        review_list = response.css('span.review-text-content span::text').extract()
        for review in review_list:
            review_item["positive_review"] = review
            review_item["amazon_item_number"] = amazon_item_number
            yield review_item


    def negative_reviews(self, response):
        url = response.url
        amazon_item_number = url.split("/")[5]
        review_item = MobilReview()
        review_list = response.css('span.review-text-content span::text').extract()
        for review in review_list:
            review_item["negative_review"] = review
            review_item["amazon_item_number"] = amazon_item_number
            yield review_item

