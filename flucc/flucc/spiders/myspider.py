import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.flucc.at/']

    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    # Method responsible for processing responses
    def parse(self, response):
        # Log the visited URL and the status code
        self.log(f"Visited {response.url} with status code {response.status}")

        # Extract interesting data using CSS selectors
        links = response.css('a[href^="/events/"]::attr(href)').getall()
        titles = response.css('div.title-dimension.h-center h4::text').getall()
        hours = response.css('div.date::text').getall()

        # Iterate over the data and yield JSON objects
        for link, title, hour in zip(links, titles, hours):
            yield {
                'Link': 'https://www.flucc.at' + link,
                'Title': title.strip(),
                'Hour': hour.strip(),
            }
