This project is based on Scrapy for scraping amazon and ebay websites.
The workflow looks like:

1. Crawled mobile phones from amazon website using Scrapy.
2. Scraped details of each mobile from amazon.
3. Scraped their positive and negative reviews..
4. Crawled mobile phones from ebay website and scraped details using Scrapy.
5. Stored scraped data of amazon and ebay in the database
6. Used Django to show the UI, the following things are shown:   
       a. The list of amazon mobiles   
       b. The review page of each mobile   
       c. Select a mobile from amazon and display the similar priced mobiles available in ebay websites.

# Setting up new Scrapy project
a. Install scrapy and user-agents libraries

To run this project:
`````
    cd WebScraperScrapy/WebScraperScrapy/
`````
b. uncomment line 24 and comment line 27 in pipeplines file to crawl amazon \
Run the spider for amazon:
`````
    scrapy crawl amazon

`````
   
c. Similarly, uncomment line 27 and comment line 24 in pipeplines file to crawl ebay \
Run the spider for ebay:
`````
    scrapy crawl ebay
`````


after this, datas will be loaded on ecommerce_items.db


# Setting up Django

For visualizing the database:

a. Install Django library. \
b. Go to project folder WebScraperDjango.
`````
    cd WebScraperDjango

`````
c. Run the Django Project:
````
    python manage.py runserver
````
d. Open http://127.0.0.1:8000/ to view it in browser
 
`````
  http://127.0.0.1:8000/

`````