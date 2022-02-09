import scrapy
from ..items import EbayItem
import re
import w3lib.html


class EbayScraper(scrapy.Spider):
    # scrap all data of samsung : ebay website
    name = 'ebay'
    page_number = 1
    start_urls = [
        'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=samsung+galaxy&_sacat=0&_sop=3'

    ]


    def parse(self, response, **kwargs):
        data = response.css("div.s-item__info")
        for i in data:
            title = i.css("h3.s-item__title--has-tags::text").extract()
            price = i.css("span.s-item__price::text").extract()
            link = i.css('a.s-item__link::attr(href)').extract()
            next = link[0]
            yield response.follow(next, self.product_detail)
        next_page = 'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=samsung+galaxy&_sacat=0&_sop=3&_pgn=' + str(
            EbayScraper.page_number)
        if EbayScraper.page_number <= 5:
            EbayScraper.page_number += 1
            yield response.follow(next_page, callback=self.parse)


    def product_detail(self, response):
        ebay_item = EbayItem()

        productprice = response.css("span.notranslate::text").extract_first()
        productprice = re.sub(r'[A-Za-z£$]+','', productprice, re.I).strip()
        productTitle = response.css("h1#itemTitle::text").extract_first()

        data = response.css('div.section td').extract()
        ebay_item['name'] = productTitle
        ebay_item['price'] = float(productprice.replace(",",""))
        ebay_item['url'] = response.url

        for i in range(len(data)):
            res = response.css('div.section td').extract()[i]
            output = w3lib.html.remove_tags(res)

            output = re.sub('\s+', '', output)

            output = re.sub('\s+', '', output)
            if output.find("MPN") != -1:
                ebay_item["mpn"] = re.sub('\s+', '',
                                          w3lib.html.remove_tags(response.css('div.section td').extract()[i + 1]))
            elif output.find("Model") != -1:
                ebay_item["model"] = re.sub('\s+', '',
                                            w3lib.html.remove_tags(response.css('div.section td').extract()[i + 1]))
            elif output.find("Screen") != -1:
                ebay_item["screen_size"] = re.sub('\s+', '', w3lib.html.remove_tags(
                    response.css('div.section td').extract()[i + 1]))
            elif output.find(("Operating")) != -1:
                ebay_item["operating_system"] = re.sub('\s+', '', w3lib.html.remove_tags(
                    response.css('div.section td').extract()[i + 1]))
            elif output.find(("Storage")) != -1:
                ebay_item["storage_capacity"] = re.sub('\s+', '', w3lib.html.remove_tags(
                    response.css('div.section td').extract()[i + 1]))

        yield ebay_item
