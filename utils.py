import json
import os
import numpy as np
import pandas as pd

def dumpjson(data, filename):
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def getdirs():

    return os.getcwd()
    

def getdata(datapath):
    
    ## -- Get the data from the JSON file into a pandas dataframe (90 entries for 90 days) --
    data_df = pd.read_json(datapath)

    ## -- Ensure correct information --
    assert data_df.shape[0] == 91, "Dataframe does not contain 90 entries / information for 90 day period! Please check the data.py."
    assert data_df.shape[1] == 3, "Dataframe missing information for one of or multiple of: prices, market_caps, total_volumes."

    ## -- Get the price, volume and market caps data as seperate dataframes --
    prices = data_df["prices"]
    volumes = data_df["total_volumes"]
    market_caps = data_df["market_caps"]

    pricesvalues = [price[1] for price in prices]
    volumesvalues = [volume[1] for volume in volumes]
    marketcapsvalues = [marketcap[1] for marketcap in market_caps]

    maxprice = max(pricesvalues)
    minprice = min(pricesvalues)
    stddevprice = np.std(pricesvalues)
    varprice = np.var(pricesvalues)
    avgprice = np.mean(pricesvalues)

    maxvolume = max(volumesvalues)
    minvolume = min(volumesvalues)
    stddevvolume = np.std(volumesvalues)
    varvolume = np.var(volumesvalues)
    avgvolume = np.mean(volumesvalues)

    maxmarketcap = max(marketcapsvalues)
    minmarketcap = min(marketcapsvalues)
    stddevmarketcap = np.std(marketcapsvalues)
    varmarketcap = np.var(marketcapsvalues)
    avgmarketcap = np.mean(marketcapsvalues)

    return prices, volumes, market_caps, maxprice, minprice, stddevprice, varprice, avgprice, maxvolume, minvolume, stddevvolume, varvolume, avgvolume, maxmarketcap, minmarketcap, stddevmarketcap, varmarketcap, avgmarketcap