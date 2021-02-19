import scrapy
import os


class LinksSpider(scrapy.Spider):
    name = "wisconsin_links"

    start_urls = [
        'https://www.dhs.wisconsin.gov/news/index.htm?items_per_page=All',
        'https://www.dhs.wisconsin.gov/news/2020.htm?items_per_page=All'
    ]

    def parse(self, response):
        links = response.css(
            '.field.field-name-title-field.field-type-text.field-label-hidden > .header-2 > a::attr(href)').getall()
        os.chdir('./links/')
        filename = 'all_wisconsin_links.txt'
        with open(filename, 'w') as f:
            f.write(','.join(links))
        os.chdir('..')
