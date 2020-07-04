### HTML Parsing
### http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html

### Task:
## Extract:
## 1. Title
## 2. Price
## 3. Quantity Available
## 4. Product Description

import requests, re, json, pprint
from lxml import html

def htmlParser(URL):
    try:
        resp = requests.get(url=URL,
             headers={
                 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                })
    except requests.exceptions.ConnectionError as e:
        print(repr(e))
    else:
        resp = resp.text.encode('ascii', 'ignore').decode('utf-8')
        tree = html.fromstring(html=resp)
        title = tree.xpath("//div[@id='content_inner']//h1/text()")[0]
        price = tree.xpath("//div[@id='content_inner']//p[@class='price_color']/text()")[0]
        availability = tree.xpath('//div[@id="content_inner"]//p[contains(@class,"availability")]/text()')[1].strip()
        in_stock = re.findall(r'\d+', availability)[0]
        description = tree.xpath('//div[@id="product_description"]/following-sibling::p/text()')[0]

        book_information = {
            'title': title,
            'price': price,
            'in_stock':in_stock,
            'description': description
        }

        pprint.pprint(json.dumps(book_information))

if __name__ == '__main__':
    htmlParser(URL="http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")