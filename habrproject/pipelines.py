import os, urllib


class HabrImagesPipeline:

    def process_item(self, item, spider):
        body = item['contents']
        path = os.path.join(os.getcwd(), 'DB', item['author_id'], item['post_id'], 'contents')
        if not os.path.exists(path):
            os.makedirs(path)
        for img in item['image_urls']:
            file_name = os.path.join(path, img[img.rfind('/') + 1:])
            # downloading image
            urllib.request.urlretrieve(img, file_name)
            # changing image link to local
            image = body.find("img", {"src": img})
            image['src'] = file_name
        return item


class HtmlWriterPipeline:

    def process_item(self, item, spider):
        # creating html file with all the information in PostItem
        index = os.path.join(os.getcwd(), 'DB', item['author_id'], item['post_id'], f'{item["post_id"]}.html')
        with open(index, 'w', encoding='utf-8') as html:
            html.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n')
            html.write(f"<h1>Author: {item['author_name']}</h1>\n")
            author_url = "https://habr.com/ru/users/" + item['author_id']
            html.write(f"<a href={author_url}>Author's page</a>\n")
            html.write(f"<a href={item['post_url']}>Original post page</a>\n")
            html.write(f"<h2>Tags: {item['tags']}</h2>\n")
            html.write(f"<h1>{item['title']}</h1>\n")
            for line in item['contents']:
                html.write(str(line) + '\n')
        return item