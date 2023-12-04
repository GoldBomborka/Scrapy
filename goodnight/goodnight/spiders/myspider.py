import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://goodnight.at/events']

    custom_settings = {
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },
        },
    }

    def parse(self, response):
        # Select all 'div.event-item-box' elements on the page
        event_boxes = response.css('div.event-item-box')

        for box in event_boxes:
            # Extract the date and remove extra spaces
            date = ' '.join(box.css('div.date::text').getall()).strip()

            # Check if the date falls among values to be skipped, if so, skip to the next record
            if date in ["4.12.23", "5.12.23", "6.12.23", "7.12.23", "8.12.23"]:
                continue

            # Extract the title ('div.title-small'), if not present, consider the text from 'a.link_new'
            title = ' '.join(box.css('div.title-small::text').getall()).strip()
            if not title:
                title = ' '.join(box.css('a.link_new::text').getall()).strip()

            # Single space between each field value
            date = ' '.join(date.split())
            title = ' '.join(title.split())

            # Return the cleaned data in a JSON record
            yield {
                'Date': date,
                'Title': title,
            }
