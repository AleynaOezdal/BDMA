# Not working due to 404 status code -> yahoo finance not scrapable

"""
def get_total_ESG():
    suffix = '.de'
    all_ratings = {}
    for company in yfinance_symbols_dax_companies:
        url = f'https://de.finance.yahoo.com/quote/{str(company+suffix).upper()}/sustainability?p={str(company+suffix).upper()}'
        print(str(company+suffix).upper())
        css_class = 'D(ib)'
        soup = bs(get(url), 'html.parser')
        print(soup)
        found_ratings = soup.find("div", attrs={"class": f"{css_class}"})
        print(found_ratings)
        count = 0
        for rating in found_ratings:
            all_ratings[f"{company}_{count}"] = rating.text
            count += 1
    return all_ratings
"""

"""for company in companies:
    url = f"https://de.finance.yahoo.com/quote/{company.upper()+'.DE'}/key-statistics?p={company.upper()+'.DE'}"
    soup = bs(get(url, yahoo_finance=True), 'html.parser')
    ebitda = soup.find_all("td", attrs={'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})
    # p.send(topic, key=f"{company}", value=ebitda.findChild('span').text) #
    # ebitda = soup.select("[class~=Fw(500) Ta(end) Pstart(10px) Miw(60px)]")
    print(f"{company.upper()+'.DE'}: {ebitda}")"""
