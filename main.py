import requests
from bs4 import BeautifulSoup

url = input('tradingview news url: ')

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')
timestamp = soup.find('div', class_='timeAndSocialShare-RYg5Gq3E timeAndSocialShare-qiFSEvvz')
print(f'timestamp: {timestamp.text}')
symbol = soup.find('span', class_="description-cBh_FN2P")
print(f'symbol: {symbol.text}')
title = soup.find('h1', class_='title-KX2tCBZq')
print(f'title: {title.text}')
article = soup.find('div', class_="body-KX2tCBZq body-pIO_GYwT content-pIO_GYwT body-RYg5Gq3E")
print(f'article: {article.text}')
