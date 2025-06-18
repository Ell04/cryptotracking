import utils
import datetime
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.cluster import DBSCAN
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from datetime import timedelta

import os
import requests

from gdeltdoc import GdeltDoc, Filters



def unix_to_datetime_string(series):
    """
    
    Convert unix time to datetime string format.

    Args:
        series (list): List of unix timestamps in milliseconds.
    
    """

    datetimevalues = [datetime.datetime.fromtimestamp(t / 1000).strftime("%Y-%m-%d") for t in series]
    return datetimevalues


def plotrawdata(prices, volumes, market_caps):
    """
    
    Plot the Raw data for prices, volumes and market caps.

    Args:
        prices (list): List of prices data.
        volumes (list): List of volumes data.
        market_caps (list): List of market caps data.
    
    """
    
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

def plotisolationforest(data, anomalies, segment):
    """
    
    Plot Isolation Forest anomaly data.

    Args:
        data (np.ndarray): The data to be plotted
        anomalies (np.ndarray): An array indicating the anomalies, where -1 indicates an anomaly
        segment (str): The segment of the data being plotted (e.g., "price",
    
    """

    sns.set_style(style="whitegrid")
    sns.set_context("notebook")
    
    ## -- Plot the anomalous data --
    plt.figure(figsize=(10, 6))

    data_df = pd.DataFrame({"Indexes": range(len(data)), 
                            "Values": data[:, 0],
                            "Anomalies": anomalies
                            })


    ## -- Get range(len(data)) for x axis (90 days) --
    ## -- data[:, 0] for y axis (Standardised price, volume, and market caps) --

    sns.scatterplot(data=data_df, x="Indexes", y="Values", 
                    hue="Anomalies", palette="viridis", s=120,
                    edgecolor="black", alpha=0.7)
    

    plt.title(f"Isolation Forest Anomalies for {segment}")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("Days (90 days)")
    plt.ylabel(f"Scaled Values for {segment}")
    plt.show()



def plotclustereddata(data, labels, segment):
    """
    
    Plot DBSCSAN clustered data.

    Args:
        data (np.ndarray): The data to be plotted
        labels (np.ndarray): An array of cluster labels, where -1 indicates noise
        segment (str): The segment of the data being plotted (e.g., "price", "volume", "market cap")
    
    """

    sns.set_style(style="whitegrid")
    sns.set_context("notebook")
    
    ## -- Plot the clustered data --
    plt.figure(figsize=(10, 6))

    data_df = pd.DataFrame({"Indexes": range(len(data)), 
                            "Values": data[:, 0],
                            "Clusters": labels
                            })

    ## -- Get range(len(data)) for x axis (90 days) --
    ## -- data[:, 0] for y axis (Standardised price, volume, and market caps) --

    sns.scatterplot(data=data_df, x="Indexes", y="Values", 
                    hue="Clusters", palette="viridis", s=120,
                    edgecolor="black", alpha=0.7)
    
    plt.title(f"DBSCAN Clustering for {segment}")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("Days (90 days)")
    plt.ylabel(f"Scaled Values for {segment}")
    plt.show()


def compute_isolation_forest(data, segment="", contamination="auto"):
    """

    Compute Isolation Forest for the given data to identify anomalies.
    The function takes the data as input and returns the indices of the anomalies. to be cross-checked with DBSCAN or similar

    Args:
        data (list): List of data points to be processed.
        segment (str): The segment of the data being processed (e.g., "price", "volume", "market cap").
        contamination (str or float): The amount of contamination in the data, default is "auto

    """

    model = IsolationForest(contamination=contamination, random_state=42)
    data = np.array([v[1] for v in data]).reshape(-1, 1)

    datalist = np.array(data)

    scaler = StandardScaler()
    datalist = scaler.fit_transform(datalist)

    model.fit(datalist)
    anomalies = model.predict(datalist)

    anomalous_indicies = np.where(anomalies == -1)[0]

    print("Anomalies detected at indicies: ", anomalous_indicies, " using isolation forest\n") if len(anomalous_indicies) > 0 else print("No isolation forest anomalies detected!\n")
    
    plotisolationforest(datalist, anomalies, segment=segment) if len(anomalous_indicies) > 0 else None
    return anomalous_indicies



def compute_dbscan(data, min_samples, eps=0.1, segment=""):
    """
    
    Compute DBSCAN clustering for the given data to identify anomalies.

    Args:
        data (list): List of data points to be processed.
        min_samples (int): The minimum number of samples in a neighborhood for a point to be considered as a core point.
        eps (float): The maximum distance between two samples for one to be considered as a neighbor
        segment (str): The segment of the data being processed (e.g., "price", "volume", "market cap"). Default is an empty string. Will be overwritten in the function call.
    
    """

    values = [v[1] for v in data]
    valuelist = np.array(values)

    scaler = StandardScaler()
    valuelist = scaler.fit_transform(valuelist.reshape(-1, 1))

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(valuelist)

    plotclustereddata(valuelist, labels, segment=segment)
    return labels, scaler, valuelist


def detect_anomalies_from_noise(data, min_samples, segment):
    """
    
    Partition the noisy data from noise labels (-1) using np.where() and return the indices of the anomalies.

    Args:
        data (list): List of data points to be processed.
        min_samples (int): The minimum number of samples in a neighborhood for a point to be considered as a core point.
        segment (str): The segment of the data being processed (e.g., "price", "volume", "market cap"). Default is an empty string. Will be overwritten in the function call.
    
    """

    labels, scaler, valuelist = compute_dbscan(data, min_samples, segment=segment)

    ## -- -1 labels are noisy in DBSCAN -- 
    anomalous_indicies = np.where(labels == -1)[0]
    return anomalous_indicies, labels, scaler, valuelist



def anomaly_pattern_detection(datapath, coin, showplots=True, priceanomalies = [], volumeanomalies = [], marketcapanomalies = []):
    """

    Call the anomaly detection functions to detect anomalies in the data and get the query parameters for each anomaly time.
    The anomalies are detected using DBSCAN clustering and the data is plotted using seaborn.
    getqueryparameters() is called to get the query parameters for each anomaly time (coin and date)

    Args:
        datapath (str): The path to the JSON file containing the data.
        coin (str): The coin for which the anomalies are to be detected (e.g., "bitcoin", "ethereum").
        showplots (bool): Whether to show the plots or not. Default is True.
        priceanomalies (list): List to store the anomalies for price data.
        volumeanomalies (list): List to store the anomalies for volume data.
        marketcapanomalies (list): List to store the anomalies for market cap data.

    """


    ## -- Unpack the data from the JSON file and basic metrics --
    prices, volumes, market_caps, \
    maxprice, minprice, stddevprice, varprice, avgprice, \
    maxvolume, minvolume, stddevvolume, varvolume, avgvolume, \
    maxmarketcap, minmarketcap, stddevmarketcap, varmarketcap, avgmarketcap = utils.getdata(datapath)
    
    ## -- Use utils script to print the metrics --
    utils.printmetrics(maxprice, minprice, stddevprice, varprice, avgprice,
                        maxvolume, minvolume, stddevvolume, varvolume, avgvolume,
                        maxmarketcap, minmarketcap, stddevmarketcap, varmarketcap, avgmarketcap)

    ## -- Plot raw data --
    plotrawdata(prices, volumes, market_caps) if showplots else None



    ## -- Detect anomalies in the data --
    ## -- Prices --

    anomalous_indicies_prices, _, _, _ = detect_anomalies_from_noise(prices, min_samples=3, segment="price") 
    print("Anomalies in price data at index: ", anomalous_indicies_prices, "\n") if len(anomalous_indicies_prices) > 0 else print("No anomalies in price data!\n")
    i_forest_prices = compute_isolation_forest(prices, segment="price")

    ## -- Volumes --

    anomalous_indicies_volumes, _, _, _ = detect_anomalies_from_noise(volumes, min_samples=3, segment="volume")
    print("Anomalies in volume data at index: ", anomalous_indicies_volumes, "\n") if len(anomalous_indicies_volumes) > 0 else print("No anomalies in volume data!\n")
    i_forest_volumes = compute_isolation_forest(volumes, segment="volume")

    ## -- Market caps --

    anomalous_indicies_mcaps, _, _, _ = detect_anomalies_from_noise(market_caps, min_samples=3, segment="market cap")
    print("Anomalies in market cap data at index: ", anomalous_indicies_mcaps, "\n") if len(anomalous_indicies_mcaps) > 0 else print("No anomalies in market cap data!\n")
    i_forest_mcaps = compute_isolation_forest(market_caps, segment="market cap")

    if len(anomalous_indicies_prices) > 0:
        anomalytime = [prices[i][0] for i in anomalous_indicies_prices]

        anomalyreadabletime = unix_to_datetime_string(anomalytime)
        print("Anomalies detected at time: ", anomalyreadabletime, " for price data")

        priceanomalies.extend(anomalyreadabletime)

    if len(anomalous_indicies_volumes) > 0:
        anomalytime = [volumes[i][0] for i in anomalous_indicies_volumes]

        anomalyreadabletime = unix_to_datetime_string(anomalytime)
        print("Anomalies detected at time: ", anomalyreadabletime, " for volume data")

        volumeanomalies.extend(anomalyreadabletime)

    if len(anomalous_indicies_mcaps) > 0:
        anomalytime = [market_caps[i][0] for i in anomalous_indicies_mcaps]

        anomalyreadabletime = unix_to_datetime_string(anomalytime)
        print("Anomalies detected at time: ", anomalyreadabletime, " for market cap data")

        marketcapanomalies.extend(anomalyreadabletime)

    else:
        print("No anomalies detected in the data!")

    
    ## -- Get the query parameters for each anomaly time --
    print("Getting price anomaly events...\n")
    getqueryparameters(priceanomalies, coin)
    time.sleep(1)


    print("Getting volume anomaly events...\n")
    getqueryparameters(volumeanomalies, coin)
    time.sleep(1)


    print("Getting market cap anomaly events...\n")
    getqueryparameters(marketcapanomalies, coin)


    return priceanomalies, volumeanomalies, marketcapanomalies


def remove404(articles):
    """
    
    Some articles from GDELT API may return 404 errors. This function checks for 404 errors and removes the articles from the list.
    The function returns a list of valid articles.

    Args:
        articles (pd.DataFrame): DataFrame containing articles with their URLs.
    
    """

    valid_articles = []

    print("\nChecking for 404 errors in articles...\n")
    assert not articles.empty, "Articles is empty! Please check search filters."

    for url in tqdm(articles["url"]):
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                valid_articles.append(url)

        except requests.RequestException as e:
            print(f"Error checking URL {url}: {e}")

    print(f"Removed {len(articles) - len(valid_articles)} articles with 404 errors.\n")
    return valid_articles 



def gdelt_query(filter, anomalytime, coin, storejson=None, gd = GdeltDoc()):
    """
    
    Conduct a GDELT query using the GDELT API and the filters provided.
    The function returns the articles and timeline data for the given anomaly time.
    The articles are stored in a JSON file and the timeline data is stored in a CSV file.

    Args:
        filter (Filters): Filters to be applied to the GDELT query.
        anomalytime (str): The time of the anomaly in the format "YYYY-MM-DD".
        coin (str): The coin for which the query is being made (e.g., "bitcoin", "ethereum").
        storejson (bool): Whether to store the articles in a JSON file or not. Default is None, which means it will not store the JSON file.
        gd (GdeltDoc): An instance of the GdeltDoc class to interact with the GDELT API.
    
    """

    ## -- Search for articles and get timeline, articles is returned as a DataFrame --
    articles = gd.article_search(filter)
    articles = remove404(articles)

    timeline = gd.timeline_search(filters=filter, mode="timelinevol")

    assert len(articles) > 0, "Articles is empty! Please check search filters."
    assert not timeline.empty, "Timeline is empty! Please check search filters."

    ## -- Dump JSON and store timeline to a csv -- 
    utils.dumpjson(articles, os.path.join(utils.getdirs(), f"data/{coin}_events/processed_events_for_{anomalytime}.json")) if storejson else None
    #timeline.to_csv("timeline.csv", index=False)



def getqueryparameters(anomalytimearr, coin):
    """
    
    Get the query parameters for each anomaly time.
    The function takes the anomaly time array and the coin as input and returns the query parameters for each anomaly time.
    The time range is 7 days before and after the anomaly time.

    Make repeated calls to gdelt_query() to get the articles and timeline data for each anomaly time.

    Args:
        anomalytimearr (list): List of anomaly times in the format "YYYY-MM-DD".
        coin (str): The coin for which the query is being made (e.g., "bitcoin", "ethereum").
    
    """

    for anomaly in range(len(anomalytimearr)):

        datestring = anomalytimearr[anomaly]
        
        ## -- Check for events in the past week centered on the amomaly date --
        anomalytimestart = datetime.datetime.strptime(datestring, "%Y-%m-%d") - timedelta(days=7)
        anomalytimestop = datetime.datetime.strptime(datestring, "%Y-%m-%d") + timedelta(days=7)

        filter = Filters(
            keyword=f"{coin}",
            start_date=anomalytimestart,
            end_date=anomalytimestop,
            num_records=20,
            language="English"
            #domain=["fool.com", "reuters.com", "bbc.co.uk", "cnn.com", "forbes.com", "cnbc.com"],
            #near=near(5, "bitcoin", "war", "trade", "economy", "inflation", "rates", "market", "cryptocurrency", "crypto"), 
            #repeat=multi_repeat([
            #    (3, "bitcoin"), 
            #    (2, "economy"), 
            #    (2, "inflation"), 
            #    (2, "stock")
            #], "OR")
        
        )
        
        gdelt_query(filter, coin=coin, storejson=True, anomalytime=anomalytimearr[anomaly])

    print("GDELT query iteration complete!\n")


if __name__ == "__main__":
    os.system("CLS")

    bitcoindatapath = os.path.join(utils.getdirs(), "data/bitcoin_data.json")
    ethereumdatapath = os.path.join(utils.getdirs(), "data/ethereum_data.json")
    choice = input("Process anomalies and events for bitcoin or ethereum? (bitcoin/ethereum): ")

    datapath = bitcoindatapath if choice.lower() == "bitcoin" else ethereumdatapath if choice.lower() == "ethereum" else None
    print("None chosen, exiting...") if datapath is None else None


    priceanomalies, volumeanomalies, marketcapanomalies = anomaly_pattern_detection(str(datapath), coin=choice.lower())