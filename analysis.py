import pandas as pd
import numpy as np
import data 
import requests
from gdeltdoc import GdeltDoc, Filters, near, repeat, multi_repeat
import json
import os
from tqdm import tqdm
import utils
import matplotlib.pyplot as plt

import datetime

'''

- Detect and analyse anomalies in the data

- Unusual patterns or events

'''

def unix_to_datetime(series):

    timestampvalues = [timestamp[0] for timestamp in series]
    data_df = pd.DataFrame(series.tolist())
    
    for time in timestampvalues:
        timestampseconds = time / 1000
        datetimevalue = datetime.datetime.fromtimestamp(timestampseconds)

        data_df = data_df.replace(to_replace=time, value=datetimevalue)


    print(data_df)


def plot(prices, volumes, market_caps):
    
    ## -- Prices data --
    pricevalue = [price[1] for price in prices]
    y = list(pricevalue)
    
    plt.plot(y, color='red', label='Price data for 90 days')
    plt.title("Raw Price Data")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

def anomaly_pattern_detection(datapath):

    ## -- Get the data from the JSON file into a pandas dataframe (90 entries for 90 days) --
    data_df = pd.read_json(datapath)

    ## -- Ensure correct information --
    assert data_df.shape[0] == 91, "Dataframe does not contain 90 entries / information for 90 day period! Please check the data.py."
    assert data_df.shape[1] == 3, "Dataframe missing information for one of or multiple of prices, market caps and total volumes."

    print(data_df)

    ## -- Get the price, volume and market caps data as seperate dataframes --
    prices = data_df["prices"]
    volumes = data_df["total_volumes"]
    market_caps = data_df["market_caps"]

    ## -- Plot some values --
    plot(prices, volumes, market_caps)

    
def gdelt_query(filters, storejson=None):

    gd = GdeltDoc()

    ## -- Search for articles and get timeline, articles is returned as a DataFrame --
    articles = gd.article_search(filters)
    timeline = gd.timeline_search(filters=filters, mode="timelinevol")

    assert not articles.empty, "Articles is empty! Please check search filters."
    assert not timeline.empty, "Timeline is empty! Please check search filters."

    ## -- Convert dataframe to dict so it can be dumped into JSON (serialisable) --
    articles_dict = articles.to_dict(orient="records")

    ## -- Dump JSON and store timeline to a csv -- 
    utils.dumpjson(articles_dict, os.path.join(utils.getdirs(), "data/processed_events.json")) if storejson else None
    timeline.to_csv("timeline.csv", index=False)

    print("Relevant articles and timelines saved!")

def getqueryparameters():
    
    ## -- TODO, 
    ## -- (1) Pass in dates of timeseries of anomaly --  
    ## -- (2) Pass in bitcoin or ethereum in case --

    filters = Filters(
        keyword="bitcoin OR ethereum",
        start_date="2023-01-01",
        end_date="2023-12-31",
        country=["UK", "US"]
        #tone=">5"
        #domain=["bbc.co.uk", "nytimes.com", "theguardian.com"],
        #near=near(5, "bitcoin", "war", "trade", "economy", "inflation", "rates", "market", "cryptocurrency", "crypto"), 
        #repeat=multi_repeat([
        #    (3, "bitcoin"), 
        #    (2, "economy"), 
        #    (2, "inflation"), 
        #    (2, "stock")
        #], "OR")
    
    )

    return filters    


if __name__ == "__main__":

    datapath = os.path.join(utils.getdirs(), "data/bitcoin_data.json")

    data_series = pd.read_json(datapath)

    unix_to_datetime(data_series['prices'])
    anomaly_pattern_detection(str(datapath))
    filters = getqueryparameters()
    gdelt_query(filters, storejson=True)