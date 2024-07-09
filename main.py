import threading
import requests
from pandas import ExcelWriter
from pandas import DataFrame
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# const
BASE_URL = 'https://th.tradingview.com'

def get_news(sb):
    # data handler
    timestamps = []
    symbols = []
    titles = []
    articles = []

    # selenium web driver
    driver = webdriver.Chrome()
    MainURL = BASE_URL + f'/symbols/SET-{sb}/news/'
    driver.get(MainURL)
    time.sleep(5)
    # bs4 web scraping
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links = soup.find_all('a',class_="card-DmjQR0Aa card-Whv2Noj0 card-o5eVjfTA")
    for link in links:
        href = link.get('href')
        r = requests.get(BASE_URL + href)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            timestamp = soup.find('div', class_='timeAndSocialShare-RYg5Gq3E timeAndSocialShare-qiFSEvvz')
            timestamps.append(timestamp.text)
            # print(f'timestamp: {timestamp.text}')
        except:
            timestamps.append('')
        try:
            symbol = soup.find('span', class_="description-cBh_FN2P")
            symbols.append(symbol.text)
            # print(f'symbol: {symbol.text}')
        except:
            symbols.append('')
        try:
            title = soup.find('h1', class_='title-KX2tCBZq')
            titles.append(title.text)
            # print(f'title: {title.text}')
        except:
            titles.append('')

        try:
            article = soup.find('div', class_="body-KX2tCBZq body-pIO_GYwT content-pIO_GYwT body-RYg5Gq3E")
            articles.append(article.text)
            # print(f'article: {article.text}')
        except:
            articles.append('')

    df = DataFrame({'timestamps': timestamps, 'symbols': symbols, 'titles': titles, 'articles': articles})
    with ExcelWriter('news.xlsx', mode="a", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sb)


if __name__ == '__main__':
    thread1 = threading.Thread(target=get_news, args=['BANPU'])
    thread2 = threading.Thread(target=get_news, args=['PTT'])
    thread3 = threading.Thread(target=get_news, args=['PTTEP'])
    thread4 = threading.Thread(target=get_news, args=['PTTGC'])
    thread5 = threading.Thread(target=get_news, args=['IRPC'])

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

    print("Scraping news finished.")
