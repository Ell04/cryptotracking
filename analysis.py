import data 
import requests
import json
import os
import utils
import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from babel.numbers import format_currency
from gdeltdoc import GdeltDoc, Filters, near, repeat, multi_repeat
from sklearn.cluster import KMeans
from tqdm import tqdm

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples

from datetime import timedelta

'''

- Detect and analyse anomalies in the data

- Unusual patterns or events

'''

def unix_to_datetime(series):

    print(series)

    datetimevalues = [datetime.datetime.fromtimestamp(t / 1000).strftime("%Y-%m-%d") for t in series]

    print("Datetime values: ", datetimevalues)
    return datetimevalues


def plotrawdata(prices, volumes, market_caps):
    
    ## -- Prices data --
    pricevalue = [price[1] for price in prices]
    y = list(pricevalue)
    
    plt.plot(y, color='red', label='Price data for 90 days')
    plt.title("Raw Price Data")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

    ## -- Volume data --
    volumevalue = [volume[1] for volume in volumes]
    y = list(volumevalue)
    
    plt.plot(y, color='red', label='Volume data for 90 days')
    plt.title("Raw Volume Data")
    plt.xlabel("Days")
    plt.ylabel("Volume")
    plt.legend()
    plt.show()

    ## -- Market cap data --
    marketcapvalue = [mcap[1] for mcap in market_caps]
    y = list(marketcapvalue)
    
    plt.plot(y, color='red', label='Market cap data for 90 days')
    plt.title("Raw Market Cap Data")
    plt.xlabel("Days")
    plt.ylabel("Market Cap")
    plt.legend()
    plt.show()


def cluster(data, n_clusters):
    values = [v[1] for v in data]
    valuelist = np.array(values)

    scaler = StandardScaler()
    valuelist = scaler.fit_transform(valuelist.reshape(-1, 1))

    kmeanscluster = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto').fit(valuelist)

    labels = kmeanscluster.labels_
    centroids = kmeanscluster.cluster_centers_

    return labels, centroids, scaler, valuelist

def silhouette_metric(data, n_clusters):
    SILHOUETTE_THRESHOLD = 0.2

    labels, centroids, scaler, valuelist = cluster(data, n_clusters)
    silhouette = silhouette_score(valuelist, labels, metric='euclidean')
    silhouette_s = silhouette_samples(valuelist, labels, metric='euclidean')

    anomalous_indicies = np.where(silhouette_s <= SILHOUETTE_THRESHOLD)[0]

    return silhouette, anomalous_indicies, labels, centroids, scaler, valuelist

def anomaly_pattern_detection(datapath, showplots=False, priceanomalies = [], volumeanomalies = [], marketcapanomalies = []):

    prices, volumes, market_caps, \
    maxprice, minprice, stddevprice, varprice, avgprice, \
    maxvolume, minvolume, stddevvolume, varvolume, avgvolume, \
    maxmarketcap, minmarketcap, stddevmarketcap, varmarketcap, avgmarketcap = utils.getdata(datapath)
    
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

    plotrawdata(prices, volumes, market_caps) if showplots else None

    ## -- Detect anomalies in the data --
    ## -- Prices --

    pricesilhouette, anomalous_indicies_prices, _, _, _, _ = silhouette_metric(prices, n_clusters=3) 

    print("Good silhouette score for price: ", pricesilhouette) if pricesilhouette > 0.5 else None
    print("Bad silhouette score for price clustering: ", pricesilhouette) if pricesilhouette <= 0.2 else None

    print("Anomalies in price data at index: ", anomalous_indicies_prices, "\n") if len(anomalous_indicies_prices) > 0 else print("No anomalies in price data!\n")

    ## -- Volumes --

    volumesilhouette, anomalous_indicies_volumes, _, _, _, _= silhouette_metric(volumes, n_clusters=3)

    print("Good silhouette score for volume: ", volumesilhouette) if volumesilhouette > 0.5 else None
    print("Bad silhouette score for volume clustering: ", volumesilhouette) if volumesilhouette <= 0.2 else None

    print("Anomalies in volume data at index: ", anomalous_indicies_volumes, "\n") if len(anomalous_indicies_volumes) > 0 else print("No anomalies in volume data!\n")

    ## -- Market caps --

    marketsilhouette, anomalous_indicies_mcaps, _, _, _, _= silhouette_metric(market_caps, n_clusters=3)

    print("Good silhouette score for market cap: ", marketsilhouette) if marketsilhouette > 0.5 else None
    print("Bad silhouette score for market cap clustering: ", marketsilhouette) if marketsilhouette <= 0.2 else None

    print("Anomalies in market cap data at index: ", anomalous_indicies_mcaps, "\n") if len(anomalous_indicies_mcaps) > 0 else print("No anomalies in market cap data!\n")

    if len(anomalous_indicies_prices) > 0:
        anomalytime = [prices[i][0] for i in anomalous_indicies_prices]

        anomalyreadabletime = unix_to_datetime(anomalytime)
        print("Anomalies detected at time: ", anomalyreadabletime, " for price data")

        priceanomalies.append(anomalyreadabletime)

    if len(anomalous_indicies_volumes) > 0:
        anomalytime = [volumes[i][0] for i in anomalous_indicies_volumes]

        print(volumes[7][0])

        anomalyreadabletime = unix_to_datetime(anomalytime)
        print("Anomalies detected at time: ", anomalyreadabletime, " for volume data")

        volumeanomalies.append(anomalyreadabletime)

    if len(anomalous_indicies_mcaps) > 0:
        anomalytime = [market_caps[i][0] for i in anomalous_indicies_mcaps]

        anomalyreadabletime = unix_to_datetime(anomalytime)
        print("Anomalies detected at time: ", anomalyreadabletime, " for market cap data")

        marketcapanomalies.append(anomalyreadabletime)

    else:
        print("No anomalies detected in the data!")




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

def getqueryparameters(anomalytime):
    
    ## -- Check for events in the past week --
    anomalytimestart = datetime.datetime.strptime(anomalytime[0], "%Y-%m-%d") - timedelta(days=7)
    anomalytimestop = datetime.datetime.strptime(anomalytime[0], "%Y-%m-%d") + timedelta(days=7)

    filters = Filters(
        keyword="bitcoin OR ethereum",
        start_date=anomalytimestart,
        end_date=anomalytimestop,
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
    os.system("CLS")

    datapath = os.path.join(utils.getdirs(), "data/bitcoin_data.json")
    data_series = pd.read_json(datapath)

    anomaly_pattern_detection(str(datapath))