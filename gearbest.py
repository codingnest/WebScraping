### https://splash.readthedocs.io/en/stable/
### JavaScript Scraping
### https://www.gearbest.com/flash-sale.html
### Task:
## Extract:
## 1. Name
## 2. URL
## 3. Original Price
## 4. Discounted Price

### Installation:
##1. docker pull scrapinghub/splash
##2. docker run -it -p 8050:8050 --rm scrapinghub/splash --max-timeout=3600

import requests
from lxml import html

extracted_data = []
def javaScriptScrapper(URL,extracted_data=[]):
    script = '''
        headers = {
            ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            ['cookie'] = 'bm_sv=8348027EADF53A62B0A88A2489F9E63A~/Z/M+RBmRemmCIlsBEfDmqtib6poRJXX7QobxdWDCOwYAJijRtzG2DcRFwGEVGBTo2oGg8NXwdvhBSyFPS6u3aO+vPZNILLcIB37Pr6pfDvInSDjZprAYED/dfjU3CWj977GaHNsIKR1PFTUcIJmIoK/scopOeqmPdS4KvJM27o=; Domain=.gearbest.com; Path=/; Max-Age=6422; HttpOnly'
        }
        splash:set_custom_headers(headers)
        splash.private_mode_enabled = false
        splash.images_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(1))
        return splash:html()
    '''

    resp = requests.post(url='http://localhost:8050/run',
                        json={
                        'lua_source': script,
                        'url': URL
                        })
    tree = html.fromstring(html=resp.content)

    deals = tree.xpath("//li[contains(@class, 'goodsItem')]/div[@class='goodsItem_content']")
    for deal in deals:
        product = {
            'name': deal.xpath(".//div[@class='goodsItem_title']/a/text()")[0].strip(),
            'url': deal.xpath(".//div[@class='goodsItem_title']/a/@href")[0],
            'original_price': deal.xpath(".//div[@class='goodsItem_delete']/del/@data-currency")[0],
            'discounted_price': deal.xpath(".//div[@class='goodsItem_detail']/span/@data-currency")[0],
        }
        extracted_data.append(product)

    print(extracted_data)

if __name__ == '__main__':
    javaScriptScrapper(URL='https://www.gearbest.com/flash-sale.html',extracted_data=[])