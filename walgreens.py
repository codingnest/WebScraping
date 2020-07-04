### https://www.walgreens.com/store/store/category/productlist.jsp?Eon=350006&fromBack=true&N=350006&o=acs
### API
### Extract
## 1. Image URL
## 2. Regular Price
## 3. Product ID
## 4. Product Display Name
## 5. Product URL

import requests, json
from urllib.parse import urljoin

def apiScraper(URL, pageNumber=1):
    url = URL
    payload = {"p": pageNumber, "s": 24, "view": "allView", "geoTargetEnabled": False,
               "abtest": ["tier2", "showNewCategories"], "deviceType": "desktop", "q": "undefined", "id": ["350006"],
               "requestType": "tier3", "sort": "Top Sellers", "couponStoreId": "15196"}

    headers = {
        'content-type': "application/json",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    data = response.json()

    try:
        products = data['products']
        for product_info in products:
            pr_info = product_info['productInfo']
            pr = {
                'img': pr_info['imageUrl'],
                'price': pr_info['priceInfo']['regularPrice'],
                'id': pr_info['prodId'],
                'name': pr_info['productDisplayName'],
                'size': pr_info['productSize'],
                'url': urljoin(base='https://walgreens.com', url=pr_info['productURL'])
            }
            extracted_products.append(pr)
        pageNumber += 1
        apiScraper(URL,pageNumber=pageNumber)
    except KeyError:
        return

if __name__ == '__main__':
    extracted_products = []
    apiScraper(URL="https://www.walgreens.com/productsearch/v1/products/search")
    print(extracted_products)
    print(len(extracted_products))

