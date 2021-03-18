# habr.com web-crawler

This web-crawler was made to collect all of the articles of indicated author(s) at habr.com for statistic purposes.
The author is defined in "start_urls" list inside of HabrSpider class in "habrspider.py" (passing url in a shell command is in development).

The result is written to the "DB" directory (DB/author/post_id/), all the images will be stored in "contents" subdirectory and also an html-file with all the contents of each article will be created.

The information that is crawled about each article is:
- author_name;
- author_id;
- title;
- post_id;
- post_url;
- tags;
- images;
- image_urls;
- contents.

The download delay is set to 10 seconds between each request to avoid ban (you can change this in habrproject/settings.py).

## How to use:

Firstly create virtual environment, activate it and install scrapy and BeautifulSoup4.

Then you can run the spider.
```shell
scrapy runspider habrproject/spiders/habrspider.py
```

## Libraries
Libraries used in this project:
- scrapy;
- re;
- BeautifulSoup4;
- json;
- os;
- urllib.

The code was written according to PEP8 and Scrapy documentation.
