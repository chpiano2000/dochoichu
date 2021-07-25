import pymongo
import pandas as pd
import argparse
from decouple import config

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="Name to export to csv")
args = vars(ap.parse_args())

url = config('URL')
client = pymongo.MongoClient(url)
db = client.crawl

data = list(db.dochoichu.find({}))
df = pd.DataFrame(data)
df.to_csv(args["name"])