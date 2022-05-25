import pymongo
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

client = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv('MONGODB.USERNAME')}:{os.getenv('MONGODB.PASSWORD')}@cluster0.hj2sr.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

databases = ["kpis", "news", "stocks"]

# Set up
db_id = client["identification"]["wkns_and_isins"]
# identification_collection = db_id["wkns_and_isins"]


def get_wkns_and_isins():
    all_json = list()
    for data in db_id.find():
        for k, v in data.items():
            print(f"Key: {k}\n Value: {v}")
            print("")
    return all_json


if __name__ == "__main__":
    # test if you get the data
    print(get_wkns_and_isins())
