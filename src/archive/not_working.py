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