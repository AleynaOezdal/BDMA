import pymongo
import os
from dotenv import load_dotenv
import certifi
from producersetup import all_companies
import pprint as pp

load_dotenv()

client = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@cluster0.hj2sr.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

databases = ["kpis", "news", "stocks"]

# Set up
db_id = client["identification"]["wkns_and_isins"]


def get_wkns_and_isins():
    all_ids = dict()
    for company in all_companies:
        all_ids[company] = db_id.find_one({"_id": company})["wkns_and_isins"]
    return all_ids


if __name__ == "__main__":
    # test if you get the data
    pp.pprint(get_wkns_and_isins())
