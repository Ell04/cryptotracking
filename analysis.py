import pandas as pd
import numpy as np


import data 
import requests
from gdeltdoc import GdeltDoc, Filters, near, repeat, multi_repeat
import json
import os
from tqdm import tqdm
import utils


'''

- Detect and analyse anomalies in the data

- Unusual patterns or events

'''


def anomaly_pattern_detection():
    pass


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
        keyword="bitcoin",
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
    
    print("Example run from self entry point")
    filters = getqueryparameters()
    gdelt_query(filters, storejson=True)