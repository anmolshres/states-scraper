import scrapy
import os


class LinksSpider(scrapy.Spider):
    name = "west_virginia_links"

    start_urls = [
        'https://oeps.wv.gov/healthalerts/Pages/default.aspx'
    ]

    def parse(self, response):
        links = response.css('td > a::attr(href)').getall()
        cutoff_idx = links.index('/healthalerts/documents/wv/WVHAN_163.pdf')
        links = links[0:cutoff_idx]
        os.chdir('./links/')
        filename = 'all_west_virginia_links.txt'
        with open(filename, 'w') as f:
            f.write(','.join(links))
        os.chdir('..')
