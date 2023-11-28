import scrapy
import json

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.daswerk.org/programm/']

    custom_settings = {
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
            },        },
    }

    def parse(self, response):
        # Retrieve all <a> elements with the specified class
        preview_links = response.css('a.preview-item--link')
        # Retrieve all <p> elements with the months
        preview_months = response.css('p.preview-item--month')
        # Retrieve all <h2> elements with the performer(s) name
        preview_headlines = response.css('h2.preview-item--headline')
        # Retrieve all <ul> elements with the information
        preview_info_lists = response.css('ul.preview-item--information')

        # Lists of links, months, performers, and information for the output file
        output_data = []

        # Loop through all <ul> elements
        for link, month, headline, info_list in zip(preview_links, preview_months, preview_headlines, preview_info_lists):
            link_text = link.css('::text').get()
            link_href = link.css('::attr(href)').get()
            month_text = month.css('::text').get()
            performer_text = headline.css('::text').get()  # We name the performer's name as Performer(s)

            # We extract all <li> elements from the current <ul> element
            info_items = info_list.css('li::text').getall()

            # We add all the data to the list
            output_data.append({'Text': link_text, 'Link': link_href, 'Month': month_text, 'Performer(s)': performer_text, 'Info': info_items})
            self.log(f"Text: {link_text}, Link: {link_href}, Month: {month_text}, Performer(s): {performer_text}, Info: {info_items}")

        # We save the links, months, performer(s) and information to the file
        return output_data
