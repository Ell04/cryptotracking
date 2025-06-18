import json
import os
import numpy as np
import pandas as pd


from babel.numbers import format_currency


def dumpjson(data, filename):
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def getdirs():

    return os.getcwd()


def printmetrics(maxprice, minprice, stddevprice, varprice, avgprice,
                 maxvolume, minvolume, stddevvolume, varvolume, avgvolume,
                 maxmarketcap, minmarketcap, stddevmarketcap, varmarketcap, avgmarketcap):

    ## -- Plot some values and basic metrics --
    print("-----------------------------\nMaximum price: ", format_currency(maxprice, 'USD', locale='en_US'))
    print("Minimum price: ", format_currency(minprice, 'USD', locale='en_US'))
    print("Standard deviation of prices: ", format_currency(stddevprice, 'USD', locale='en_US'))
    print("Variance of prices: ", format_currency(varprice, 'USD', locale='en_US'))
    print("Average price: ", format_currency(avgprice, 'USD', locale='en_US'), "\n-----------------------------")


    print("Maximum volume: ", format_currency(maxvolume, 'USD', locale='en_US'))
    print("Minimum volume: ", format_currency(minvolume, 'USD', locale='en_US'))
    print("Standard deviation of volumes: ", format_currency(stddevvolume, 'USD', locale='en_US'))
    print("Variance of volumes: ", format_currency(varvolume, 'USD', locale='en_US'))
    print("Average volume: ", format_currency(avgvolume, 'USD', locale='en_US'), "\n-----------------------------")

    print("Maximum market cap: ", format_currency(maxmarketcap, 'USD', locale='en_US'))
    print("Minimum market cap: ", format_currency(minmarketcap, 'USD', locale='en_US'))
    print("Standard deviation of market cap: ", format_currency(stddevmarketcap, 'USD', locale='en_US'))
    print("Variance of market cap: ", format_currency(varmarketcap, 'USD', locale='en_US'))
    print("Average market cap: ", format_currency(avgmarketcap, 'USD', locale='en_US'), "\n-----------------------------")

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