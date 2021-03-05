import cld2
from datetime import datetime
from tika import parser
import re

linksFile = open('./links/all_west_virginia_links.txt', 'r')
pattern_link = r';;.*'
pattern_title = r'.*;;'
saved_list = list(linksFile.read().split(','))
final_links = list(map(lambda saved: 'https://oeps.wv.gov' +
                       re.sub(pattern_link, '', saved), saved_list))
title_links = list(map(lambda saved: re.sub(
    pattern_title, '', saved), saved_list))
posts = []

for link in final_links:
    if link.endswith('.pdf'):
        now = datetime.utcnow().replace(microsecond=0).isoformat()
        datetimeToday = now + 'Z'
        parsed_pdf = parser.from_file(link)
        text = parsed_pdf['content']
        date = parsed_pdf['metadata']['Last-Modified']
        date = re.sub(r'T.*', '', date)
        idx = final_links.index(link)
        title = title_links[idx]
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        source = 'West Virginia Office of Epidemiology and Prevention Services'
        obj_to_add = {
            'title': title,
            'source': source,
            'published': date,
            'url': link,
            'scraped': datetimeToday,
            'classes': ['Government'],
            'country': 'United States of America',
            'municipality': 'West Virginia',
            'language': language,
            'text': text
        }
        posts.append(obj_to_add)

file = open('posts/west_virginia_posts.json', 'w+', encoding='utf-8')
file.write(str(posts))
file.close()
