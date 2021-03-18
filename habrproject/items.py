import scrapy


class PostItem(scrapy.Item):
    title = scrapy.Field()
    post_id = scrapy.Field()
    author_name = scrapy.Field()
    author_id = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field() # this field is used in Images Pipeline to store the results
    contents = scrapy.Field()
    post_url = scrapy.Field()