import scrapy
from scrapy.pipelines.images import ImagesPipeline
import re
from bs4 import BeautifulSoup as bs
import json
import os
import urllib
from habrproject.items import PostItem
from habrproject import settings as spider_settings


class HabrSpider(scrapy.Spider):
    name = 'habr'

    start_urls = [
        'https://habr.com/ru/users/vconst/posts/',
        'https://habr.com/ru/users/stefanbuzz/posts/',
    ]


    def parse(self, response):
        post_links = response.css('h2.post__title a::attr(href)')
        yield from response.follow_all(post_links, self.parse_posts)

        next_page = response.css('li.arrows-pagination__item a::attr(href)').getall()
        is_next = response.css('li.arrows-pagination__item a::attr(id)').getall()

        # check whether this is the last page
        # if it is then the spider stops
        if 'next_page' in is_next:
            # for going from 1st page to 2nd
            if len(next_page) == 1:
                next_page = response.urljoin(next_page[0])
                yield scrapy.Request(next_page, callback=self.parse)
            # for going 2nd to 3rd page and further
            elif len(next_page) == 2:
                next_page = response.urljoin(next_page[1])
                yield scrapy.Request(next_page, callback=self.parse)


    def parse_posts(self, response):
        # this function will be triggered for each individual post
        post = response.text
        soup = bs(post, 'html.parser')
        post_details = json.loads(soup.find('script', type="application/ld+json").string)
        post_contents = soup.find('div', id="post-content-body")
        author_id = response.css('span.user-info__nickname::text').get()
        post_id = re.sub(r'\D', '', response.url)
        post_info = PostItem()
        post_info['title'] = response.css('title::text').get()
        post_info['post_id'] = post_id
        post_info['author_name'] = post_details['author']['name']
        post_info['author_id'] = author_id
        post_info['tags'] = post_details['about']
        post_info['image_urls'] = post_details['image']
        post_info['contents'] = post_contents
        post_info['post_url'] = response.url
        path = os.path.join(os.getcwd(), 'DB', author_id, post_id, 'contents')
        if not os.path.exists(path):
            os.makedirs(path)
        yield post_info
