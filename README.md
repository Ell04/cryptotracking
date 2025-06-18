# Cryptotracking

## Description

Cryptotracking retrieves price, volume and market cap series data for Ethereum and Bitcoin from the CoinGecko API and uses techniques such as DBSCAN and IsolationForests to identify anomalies in the data. The anomalies are plotted and a date range for the anomaly is entered into GDELT to attempt to contextualise the anomaly by returning potentially relevant articles. Furthermore, experimentation with GenerativeAI / GPT for these dates have also been explored in an attempt to semantically understand anomalies further than statistical findings.

## Structure

- `data.py`: Retrieves data from the CoinGecko API for Ethereum, Bitcoin, or both at once.
- `analysis.py`: Finds and analyses the anomalies using DBSCAN and isolation forests, and passes data for GDELT queries. Converts Unix timestamps to human readable dates for the GDELT queries. Plots anomaly data using seaborn.

- `semantics.py`: Boilerplate code for GPT requests for the anomaly date.
- `utils.py`: Helper functions that are reused. Computes basic stats for the data and dumps JSON.

- `prompt.txt`: Example GPT prompt.

- `data/`: Contains JSON files for processed GDELT articles (URLs) for anomaly date periods (e.g `data/bitcoin_events`) and coin prices, volumes and market caps (e.g `data/bitcoin_data.json`).