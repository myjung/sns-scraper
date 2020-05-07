import scrapy


class DcSpider(scrapy.Spider):
    name = 'dcinside'

    def start_requests(self):
        urls = [
            "https://gall.dcinside.com/board/lists/?id=mcdonalds&page=1",
            "https://gall.dcinside.com/board/lists/?id=mcdonalds&page=2"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        print(page)
