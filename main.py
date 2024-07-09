import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time


driver = webdriver.Chrome()
MainURL = input('Sub Url : ')
driver.get(MainURL)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'lxml')
links = soup.find_all('a',class_="card-DmjQR0Aa card-Whv2Noj0 card-o5eVjfTA")
for link in links:
    href = link.get('href')
    r = requests.get('https://th.tradingview.com' + href)
    soup = BeautifulSoup(r.content, 'lxml')

    timestamp = soup.find('div', class_='timeAndSocialShare-RYg5Gq3E timeAndSocialShare-qiFSEvvz')
    print(f'timestamp: {timestamp.text}')
    symbol = soup.find('span', class_="description-cBh_FN2P")
    print(f'symbol: {symbol.text}')
    title = soup.find('h1', class_='title-KX2tCBZq')
    print(f'title: {title.text}')
    article = soup.find('div', class_="body-KX2tCBZq body-pIO_GYwT content-pIO_GYwT body-RYg5Gq3E")
    print(f'article: {article.text}')