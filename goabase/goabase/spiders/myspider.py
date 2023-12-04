import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.goabase.net/party/?saAtt[geoloc]=wien&saAtt[radius]=100&saAtt[geolat]=48.2&saAtt[geolon]=16.3']

    custom_settings = {
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        # Scraping the main page
        self.logger.info(f"Scraping main page: {response}")

        # Extracting links to individual party pages
        links = response.css('a.party-link::attr(href)').getall()

        # Following each link to the party page
        for link in links:
            yield response.follow(link, callback=self.parse_party)

    def parse_party(self, response):
        # Scraping an individual party page
        self.logger.info(f"Scraping party page: {response}")

        # Extracting the title from the party page
        title = response.css('span.block.strong.over-hidden::text').get()

        # Yielding the result
        yield {
            'Link': response,
            'Title': title,
        }
