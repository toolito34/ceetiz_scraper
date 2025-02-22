import scrapy
import requests
from scrapy_playwright.page import PageMethod

class CeetizSpider(scrapy.Spider):
    name = "ceetiz"
    start_urls = ["https://www.ceetiz.fr/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [PageMethod("wait_for_selector", "div.relative.flex.flex-col")]
                }
            )

    async def parse(self, response):
        for activity in response.css("div.relative.flex.flex-col"):
            data = {
                "title": activity.css("p[title]::text").get(),
                "price": activity.css("span.font-bold.text-primary::text").get(),
                "location": activity.css("div.text-yellow-400.text-sm::text").get(),
                "image": activity.css("figure img::attr(src)").get(),
                "url": response.urljoin(activity.css("a::attr(href)").get())
            }
            requests.post("http://127.0.0.1:8000/activities/", json=data)