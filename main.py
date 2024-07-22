import threading
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

# const
APIPath = 'https://news-headlines.tradingview.com/headlines/?lang=th&symbol=SET%3A'
BaseURL = 'https://th.tradingview.com'

def get_news(sb):
    timestamps = []
    symbols = []
    titles = []
    articles = []
    response = requests.get(APIPath+sb)
    if response.status_code != 200: print('API Error')
    data = response.json()
    links = [headline['storyPath'] for headline in data]
    for link in links:
        r = requests.get(BaseURL+link)
        soup = BeautifulSoup(r.content,'lxml')
        try:
            timestamp = soup.find('div', class_='timeAndSocialShare-RYg5Gq3E timeAndSocialShare-qiFSEvvz')
            timestamps.append(timestamp.text)
            # print(f'timestamp: {timestamp.text}')
        except:
            print(f'{sb} timestammp error')
            timestamps.append('ERROR')
        
        try:
            symbol = soup.find_all('span', class_="description-cBh_FN2P")
            temp = []
            for s in symbol:
                temp.append(s.text)
            symbols.append(','.join(temp))

        except:
            print(f'{sb} symbol error')
            symbols.append('ERROR')
        
        try:
            title = soup.find('h1', class_='title-KX2tCBZq')
            titles.append(title.text)

        except:
            print(f'{sb} title error')
            titles.append('ERROR')

        try:
            article = soup.find('div', class_="body-KX2tCBZq body-pIO_GYwT content-pIO_GYwT body-RYg5Gq3E")
            articles.append(article.text)

        except:
            print(f'{sb}: article error')
            articles.append('ERROR')
            continue

    df = DataFrame({'timestamps': timestamps, 'symbols': symbols, 'titles': titles, 'articles': articles})
    # with ExcelWriter('news.xlsx', mode="a", engine="openpyxl") as writer:
    file = sb.lower() + '_news.csv'
    df.to_csv(file, encoding='utf-8', index=False)
    print(file + ' is done')


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
