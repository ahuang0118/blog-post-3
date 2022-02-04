# to run 
# scrapy crawl imdb_spider -o movies.csv

from urllib.request import Request
import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0108778/']

    def parse(self,response):
        full_credits = response.urljoin("fullcredits")
        yield scrapy.Request(full_credits, callback = self.parse_full_credits)
    
    def parse_full_credits(self,response):
        actor_pages = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for page in actor_pages:
            actcor_page = response.urljoin(page)
            yield scrapy.Request(actcor_page, callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        actor_name = response.css("h1.header").css("span.itemprop::text").get()
        for a in response.css("div.filmo-row b").css("a::text"):
            movie_or_TV_name = a.get()
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}






