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
def get_news_headlines_from_finanzennet():
    dax40_companies = ['adidas', 'sap', 'bmw']

    for company in dax40_companies:
        base_url = f'https://www.finanzen.net/news/{company}-news'
        print(f"Now following company: {company}")
        soup = bs(get(base_url), 'html.parser')

        # Top Headlines on website
        content = soup.find('span', attrs={"class": "teaser-headline"})
        print(content.text)

        # List Headlines on website
        found_news = soup.find_all("a", attrs={"class": "teaser"})
        for headline in found_news:
            print(f"{headline.text}")
        print(f"+++ Finished Company: {company} +++\n")


if __name__ == '__main__':
    get_news_headlines_from_finanzennet()
