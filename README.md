# Cryptotracking 🪙

Tracking Cryptocurrencies and understanding their price fluctuations.

## Overview 📖

Cryptotracking retrieves price, volume and market cap series data for Ethereum and Bitcoin from the [`CoinGecko API`](https://www.coingecko.com/en/api) and uses techniques such as [`DBSCAN`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) and [`IsolationForests`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) to identify anomalies in the data. The anomalies are plotted and a date range for the anomaly is entered into [`GDELT`](https://www.gdeltproject.org/) to attempt to contextualise the anomaly by returning potentially relevant articles, and analysis is further enriched by LLMs extracting semantic reasoning behind potential causes.

## Features 📲

The repository allows for the gathering of Bitcoin and Ethereum price data, market cap data and volume data for a 90-day period. This data which is processed into [`json files`](data/bitcoin_data.json) is passed to the GDELT API in human readable format to get a date range for articles relating to cryptocurrency. This is then further given to an LLM to validate these sources. Additionally, LLMs may also contextualise the anomaly and find resources for the explaination themselves.



## Structure 🏗️

- [`data.py`](data.py): Retrieves data from the CoinGecko API for Ethereum, Bitcoin, or both at once.
- [`analysis.py`](analysis.py): Finds and analyses the anomalies using DBSCAN and isolation forests, and passes data for GDELT queries. Converts Unix timestamps to human readable dates for the GDELT queries. Plots anomaly data using seaborn.

- [`utils.py`](utils.py): Helper functions that are reused. Computes basic stats for the data and dumps JSON.

- [`plothandler.py`](plothandler.py): Creates a local HTML page to display all the plots

- [`runner.py`](runner.py): Runner script to execute the code

## Requirements ✔️

Please find the requirements in [`requirements.txt`](requirements.txt)

## Usage 🔨

...