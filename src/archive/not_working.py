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


"""
def get_stock_price(companies: list = all_companies):

    for company in companies:
        comp_stock_prices = dict()
        try:
            base_url = f"https://www.finanzen.net/aktien/{company}-aktie"
            soup = bs(get(base_url), "html.parser")

            stock_price = {
                "price": soup.find("div", {"class": "row quotebox"})
                .find_all("div")[0]
                .text,
                "change": soup.find("div", {"class": "row quotebox"})
                .find_all("div")[2]
                .text,
                "open": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[5]
                .text.split()[0],
                "day_before": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[5]
                .text.split()[2],
                "highest": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[11]
                .text.split()[0],
                "lowest": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[11]
                .text.split()[2],
                "marketcap": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[9]
                .text,
                "time": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[3]
                .text.split()[1],
                "date": soup.find("div", {"class": "box table-quotes"})
                .find_all("td")[3]
                .text.split()[0],
            }

            comp_stock_prices[f"{company}"] = stock_price

        except Exception as e:
            comp_stock_prices[f"{company}"] = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Store company as key and stock price as value in a dict and transform it into JSON
        p.produce(
            "current_stock_price",
            json.dumps(
                {
                    "_id": company,
                    "stock_price": comp_stock_prices,
                    "time": str(dt.datetime.now()),
                }
            ),
            callback=delivery_report,
        )
        p.flush()

    return "Done. Produced all Stock Prices to Kafka."
"""
