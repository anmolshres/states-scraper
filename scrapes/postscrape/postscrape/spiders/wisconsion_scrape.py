# Regex to getting New Zealand links
# https://regex101.com/r/MxoFhB/1
###

import scrapy
import html2text
import cld2
import dateparser
from datetime import datetime


class PostsSpider(scrapy.Spider):
    linksFile = open('./links/all_wisconsin_links.txt', 'r')

    name = "wisconsin_posts"
    start_urls = map(lambda link: 'https://www.dhs.wisconsin.gov' + link if link.startswith(
        'http') == False else link, linksFile.read().split(','))

    def parse(self, response):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        url = response.url
        datetimeToday = now + 'Z'
        contentElement = response.css('article').get()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css('.release-date::text').get()
        updatedDate = dateparser.parse(date).date()
        titleElement = response.css('title::text').get()
        title = titleElement[:-42]
        text = converter.handle(contentElement)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        source = titleElement[-39:]
        yield{
            'title': title,
            'source': source,
            'published': updatedDate,
            'url': url,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'United States of America',
            'municipality': 'Wisconsin',
            'language': language,
            'text': text
        }
