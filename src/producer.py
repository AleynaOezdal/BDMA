from bs4 import BeautifulSoup as bs
import json
from producersetup import all_companies, delivery_report, get, p


def get_stock_price(companies: list = all_companies):

    for company in companies:
        comp_stock_prices = dict()
        try:
            base_url = f'https://www.finanzen.net/aktien/{company}-aktie'
            soup = bs(get(base_url), 'html.parser')

            stock_price = {
                "price": soup.find("div", {"class": "row quotebox"}).find_all("div")[0].text,
                "change": soup.find("div", {"class": "row quotebox"}).find_all("div")[2].text,
                "open": soup.find("div", {"class": "box table-quotes"}).find_all("td")[5].text.split()[0],
                "day_before": soup.find("div", {"class": "box table-quotes"}).find_all("td")[5].text.split()[2],
                "highest": soup.find("div", {"class": "box table-quotes"}).find_all("td")[11].text.split()[0],
                "lowest": soup.find("div", {"class": "box table-quotes"}).find_all("td")[11].text.split()[2],
                "marketcap": soup.find("div", {"class": "box table-quotes"}).find_all("td")[9].text,
                "time": soup.find("div", {"class": "box table-quotes"}).find_all("td")[3].text.split()[1],
                "date": soup.find("div", {"class": "box table-quotes"}).find_all("td")[3].text.split()[0],
            }

            comp_stock_prices[f"{company}"] = stock_price

        except Exception as e:
            comp_stock_prices[f"{company}"] = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Store company as key and stock price as value in a dict and transform it into JSON
        p.produce('stock_price', json.dumps({str(company): comp_stock_prices}), callback=delivery_report)
        p.flush()

    return "Done. Produced all Stock Prices to Kafka."


def get_news(companies: list = all_companies):

    for company in companies:

        try:
            base_url = f"https://www.finanzen.net/aktien/{company}-aktie"
            soup = bs(get(base_url), 'html.parser')
            found_news = soup.find("div", {"class": "col-sm-8 col-xs-12"}).find_all("div", {"class": "newsTeaser clearfix"})
            count = 0
            for headline in found_news:
                news = dict()
                headline_news = {
                    "headline": headline.find("div", {"class": "newsTeaserText"}).find("a").text,
                    "timestamp": headline.find("div", {"class": "pull-left"}).text,
                    "more_info": "https://www.finanzen.net/nachricht/aktien/" +
                                 headline.find("div", {"class": "newsTeaserText"}).a["href"],

                }
                # Generate unique key with company and iterating count
                # Store headline as value for specific key
                news[f"{company}_{count}"] = headline_news
                count += 1
                # Store company as key and headline as value in a dict and transform it into JSON
                p.produce('news', json.dumps({str(company): news}), callback=delivery_report)
                p.flush()

        except Exception as e:
            # Because there a lots of news for each DAX company, we don't produce a failed news item to Kafka
            print(f"FAILED. For {company} the following error occured: {type(e)}")
            continue

    return "Done. Produced all News to Kafka."


def get_worker_review(companies: list = all_companies):

    for company in companies:
        all_reviews = dict()
        try:
            base_url = f"https://www.kununu.com/de/{company}"
            soup = bs(get(base_url), 'html.parser')
            kununu_positive = soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"}).find("div", {
            "id": "summary-employees-like"}).find_all("div", {"class", "index__snippet__35vvF"})
            kununu_negative = soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"}).find("div", {
            "id": "summary-employees-dont-like"}).find_all("div", {"class", "index__snippet__35vvF"})
            kununu_suggestions = soup.find("div", {"class": "index__whatEmployeesSayContent__3RF4U"}).find("div", {
            "id": "summary-employees-suggestions"}).find_all("div", {"class", "index__snippet__35vvF"})

            count = 0
            for review in kununu_positive:
                positive = {
                    "positive": review.find("q").text,
                    "more info": "https://www.kununu.com" + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a["href"]
                }
                all_reviews[f"{company}_{count}"] = positive
                count += 1
                post = {f"{company}_{count}": positive}
                all_reviews.update(post)
            for review in kununu_negative:
                negative = {
                    "negative": review.find("q").text,
                    "more info": "https://www.kununu.com" + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a["href"]
                }
                all_reviews[f"{company}_{count}"] = negative
                count += 1
                post = {f"{company}_{count}": negative}
                all_reviews.update(post)
            for review in kununu_suggestions:
                suggestions = {
                    "suggestions": review.find("q").text,
                    "more info": "https://www.kununu.com" + review.find("div", {"class": "index__snippetInfo__1OMUQ"}).a["href"]
                }
                all_reviews[f"{company}_{count}"] = suggestions
                count += 1
                post = {f"{company}_{count}": suggestions}
                all_reviews.update(post)

        except Exception as e:
            all_reviews[f'{company}'] = "NaN"
            print(f"FAILED. For {company} the following error occured: {type(e)}")

        # Store company as key and Reviews as value in a dict and transform it into JSON
        p.produce('Reviews', json.dumps({str(company): all_reviews}), callback=delivery_report)
        p.flush()
    return "Done. Produced all Reviews to Kafka."

def get_world_news():
    try:
        base_url = "https://www.boerse.de/unternehmensnachrichten/welt/"
        soup = bs(get(base_url), 'html.parser')

        found_news = soup.find("div", {"class": "newsKasten inhaltsKasten"}).find_all("div", {"class": "row row-bordered"})

        count = 0

        for headline in found_news:
            news = dict()
            if headline.find("div", {"class": "col-xs-9 col-md-10"}) == EOFError:
                continue
            else:
                headline_news = {
                    "headline": headline.find("div", {"class": "col-xs-9 col-md-10"}).find("a").text.replace("  ", "").replace("\n",""),
                    "timestamp": headline.find("div", {"class": "col-xs-3 col-md-2"}).text.replace("  ", "").replace("\n", ""),
                    "more_info": headline.find("div", {"class": "col-xs-9 col-md-10"}).a["href"],
                 }
                # Store as key and news as value in a dict
                news[f"Welt-News_{count}"] = headline_news
                count += 1
                # Transform dict into JSON and produce it to Kafka
                p.produce('world_news', json.dumps(news), callback=delivery_report)
                p.flush()

    except Exception as e:
        # Since general news are existing in high quantity, we won't produce here anything to Kafka.
        print(f"FAILED. For Welt-News the following error occured: {type(e)}")

    return "Done. Produced all World-news to Kafka."


def get_community(companies, number): #Liste für companies und number erstellen

    for company in companies[0], number:
        community = dict()
        try:
            base_url = f"https://www.boersennews.de/community/diskussion/{company}/{number}/#moreComments"
            soup = bs(get(base_url), 'html.parser')

            count = 0

            found_community = soup.find("div", {"class":"row row-cols-1 g-3 mt-0 justify-content-end"}).find_all("div", {"class":"row g-3 mt-0 userPosting"})

            for chat in found_community:
                communities = {
                            "message": chat.find("div", {"class":"text-info text-break overflow-auto pe-3"}).text.replace("  ", "").replace("\r", "").replace("\n", "").replace("\t", ""),
                            "timestamp" : chat.find("small", {"class":"d-block text-truncate"}).text.split()[2].replace("  ", "").replace("\r", "").replace("\n", "").replace("\t", ""),
                            "User": chat.find("small", {"class": "d-block text-truncate"}).text.split()[0].replace("  ", "").replace("\r", "").replace("\n", "").replace("\t", ""),
                            "more info": base_url
                        }
                community[f"{company}_{count}"] = communities
                count += 1
                post = {f"{company}_{count}": communities}
                community.update(post)
        except Exception as e:
            community = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")
        # Store company as key and WKN/ISIN as value in a dict and transform it into JSON

        p.produce('Community_news', json.dumps({str(company): community}), callback=delivery_report)
        p.flush()
    return "Done. Produced all Community_news to Kafka."


def get_customer_experience(companies):
    for company in companies:
        customer_exp = dict()
        try:
            # TBD: URLs
            base_url = f"https://de.trustpilot.com/review/{company}"
            soup = bs(get(base_url), 'html.parser')

            count = 0

            found_cus_exp = soup.find("section", {"class":"styles_reviewsContainer__3_GQw"}).find_all("section", {"class":"styles_reviewContentwrapper__zH_9M"})

            for experience in found_cus_exp:
                cus_exp = {
                    "title": experience.find("a").text,
                    "review": experience.find("div", {"class": "styles_reviewContent__0Q2Tg"}).contents[-1].text,
                    "time": experience.find("div", {"class": "typography_typography__QgicV typography_bodysmall__irytL typography_color-gray-6__TogX2 typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3 styles_datesWrapper__RCEKH"}).text,
                    "more info": base_url + experience.a["href"]
                }
                customer_exp[f"{company}_{count}"] = cus_exp
                count += 1
                post = {f"{company}_{count}": cus_exp}
                customer_exp.update(post)
        except Exception as e:
            customer_exp = 'NaN'
            print(f"FAILED. For {company} the following error occured: {type(e)}")
        # Store company as key and WKN/ISIN as value in a dict and transform it into JSON

        p.produce('Customer_experience', json.dumps({str(company): customer_exp}), callback=delivery_report)
        p.flush()
    return "Done. Produced all Customer_experience to Kafka."



if __name__ == '__main__':
    # Next steps: Every headline as single message to KAFKA
    # WARN: Only start if kafka cluster is set up!
    pass