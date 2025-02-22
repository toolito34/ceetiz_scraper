import scrapy
import requests
from scrapy_playwright.page import PageMethod

class CeetizSpider(scrapy.Spider):
    name = "ceetiz"
    start_urls = ["https://www.ceetiz.fr/new-york/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [PageMethod("wait_for_selector", "section.card-shadow")]
                }
            )

    async def parse(self, response):
        for activity in response.css("section.card-shadow"):
            title = activity.css("p[title]::text").get()
            price = activity.css("span.font-bold.text-primary::text").get()
            location = "New York"
            image = activity.css("img::attr(src)").get()
            url = response.urljoin(activity.css("a::attr(href)").get())

            self.logger.info(f"Titre: {title}")
            self.logger.info(f"Prix: {price}")
            self.logger.info(f"Lieu: {location}")
            self.logger.info(f"Image: {image}")
            self.logger.info(f"URL: {url}")

            data = {
                "title": title,
                "price": price,
                "location": location,
                "image": image,
                "url": url
            }
            # Vérifier que toutes les données sont présentes avant d'envoyer la requête
            if all(data.values()):
                self.logger.info(f"Envoi des données: {data}")
                try:
                    response = requests.post("http://127.0.0.1:8000/activities/", json=data)
                    self.logger.info(f"Réponse de l'API: {response.status_code}")
                except requests.RequestException as e:
                    self.logger.error(f"Erreur lors de l'envoi des données: {e}")
            else:
                self.logger.warning(f"Données incomplètes pour l'activité: {data}")