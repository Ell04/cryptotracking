import json
import os
import numpy as np
import pandas as pd
import yaml

from babel.numbers import format_currency

config_path = os.path.join(os.path.dirname(__file__), "api_config.yml")

def get_key(service, config_file="api_config.yml"):
    """
    Get API key

    Args:
        service (str): The name of the service to get the API key for.
        config_file (str): The path to the configuration file.

    Returns:
        str: The API key for the specified service.
    """

    if not os.path.exists(config_file):
        config_file = config_path

    ## -- Read the YML file first and get the right entry
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config[service]["key"]

def dumpjson(data, filename):
    """

    Simple JSON dump function.

    Args:
        data (dict): The data to dump.
        filename (str): The name of the file to dump the data to.

    Returns:
        None
    """
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def getdirs():

    return os.getcwd()


def printmetrics(maxprice, minprice, stddevprice, varprice, avgprice,
                 maxvolume, minvolume, stddevvolume, varvolume, avgvolume,
                 maxmarketcap, minmarketcap, stddevmarketcap, varmarketcap, avgmarketcap):
    
    """
    
    Handle cumbersome printing of simple metrics extracted from 90 day cryptocurrency data

    Args:
        maxprice (float): The maximum price.
        minprice (float): The minimum price.
        stddevprice (float): The standard deviation of prices.
        varprice (float): The variance of prices.
        avgprice (float): The average price.
        maxvolume (float): The maximum volume.
        minvolume (float): The minimum volume.
        stddevvolume (float): The standard deviation of volumes.
        varvolume (float): The variance of volumes.
        avgvolume (float): The average volume.
        maxmarketcap (float): The maximum market cap.
        minmarketcap (float): The minimum market cap.
        stddevmarketcap (float): The standard deviation of market cap.
        varmarketcap (float): The variance of market cap.
        avgmarketcap (float): The average market cap.

    """

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