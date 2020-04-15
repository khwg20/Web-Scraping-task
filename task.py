import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv
filecsv = open('AlibabaData.csv', 'w', encoding='utf8')
# Set the URL you want to webscrape from
url = 'https://www.alibaba.com/products/stiker.html?spm=a2700.galleryofferlist.0.0.16625853MvvHTb&IndexArea=product_en&page='
file = open('AlibabaData.json', 'w', encoding='utf8')
file.write('[\n')
data = {}
csv_columns = ['name', 'price', 'img', 'rate', 'SllerAge']
for page in range(15):
    print('---', page, '---')
    r = requests.get(url + str(page))
    print(url + str(page))
    soup = BeautifulSoup(r.content, "html.parser")
    ancher = soup.find_all(
        'div', {'class': 'organic-list-offer-outter J-offer-wrapper'})
    writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
    i = 0
    writer.writeheader()
    for pt in ancher:
        name = pt.find('p', {'class': 'organic-gallery-title__content medium'})
        itemPrice = pt.find('p', {'class': 'gallery-offer-price medium'})
        img = pt.find('img', {'class': 'J-img-switcher-item'})
        rate = pt.find('span', {'class': 'seb-supplier-review__score'})
        SllerAge = pt.find(
            'span', {'class': 'seller-tag__year list-offer-seller-tag'})
        if img:
            writer.writerow({'name': name.text.replace('                    ', '').strip(
                '\r\n'), 'price': itemPrice.text, 'img': img.get('src')})
            data['name'] = name.text.replace(
                '                    ', '').strip('\r\n')
            data['price'] = itemPrice.text
            data['img'] = img.get('src')

            data['SllerAge'] = SllerAge.text
            json_data = json.dumps(data, ensure_ascii=False)
            file.write(json_data)
            file.write(",\n")
file.write("\n]")
filecsv.close()
file.close()
