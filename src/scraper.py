import requests
from bs4 import BeautifulSoup as bs

# Crawling web page with given URL
def get(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text.strip()
    else:
        return 'Error in URL Status Code'

# Parsing html
def get_news_headline(url):
    parser = bs(get(url), 'html.parser')
    print(parser.prettify())


if __name__ == '__main__':
    get_news_headline('https://www.finanzen.net/news/adidas-news')