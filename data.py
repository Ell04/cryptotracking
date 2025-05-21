import pandas as pd
import numpy as np
import requests
import json
import utils
import os

'''

Prepare the data:

- Retrieve daily price and volume series for Bitcoin and Ethereum (90 days) 
- CoinGecko API

'''

class cryptodata:
    def __init__(self, coin, storejson=True):

        ## -- Store coin variable and url dictionary internally --
        self.coin = coin
        self.urls = self.get_data_urldict()

        ## -- Get the filename to store the data based on user's local machine directory and validate --)
        self.validate()

        try:
            
            ## -- From https://docs.coingecko.com/v3.0.1/reference/coins-id-market-chart --
            print(f"Retrieving data for {self.coin} ethereum and bitcoin...") if self.coin == "both" else print(f"Retrieving data for {self.coin}...")

            if self.coin == "both":
                
                ## -- Get URL from the dictionary for both coins --
                ethurl = self.urls["ethereum"]
                btcurl = self.urls["bitcoin"]

                ## -- Set headers for the requests for both coins --
                ethereumresponse = requests.get(ethurl, headers={"accept": "application/json"}, timeout=10)
                bitcoinresponse = requests.get(btcurl, headers={"accept": "application/json"}, timeout=10)

                ## -- Get response --
                self.ethereumdata = ethereumresponse.json()
                self.bitcoindata = bitcoinresponse.json()

                ## -- Check for a valid nonempty response --
                assert self.ethereumdata, "No data found for ethereum."
                assert self.bitcoindata, "No data found for bitcoin."
                
                print(f"Data retrieved successfully for {self.coin} bitcoin and ethereum.")

                self.storejson(self.ethereumdata, os.path.join(utils.getdirs(), "data/ethereum_data.json")) if storejson else None
                self.storejson(self.bitcoindata, os.path.join(utils.getdirs(), "data/bitcoin_data.json")) if storejson else None

            elif self.coin == "bitcoin" or self.coin == "ethereum":

                ## -- Get URL from the dictionary --
                url = self.urls[self.coin]

                ## -- Set headers for the request --
                headers = {"accept": "application/json"}

                ## -- Make the API request and get the response as JSON --
                apiresponse = requests.get(url, headers=headers, timeout=10)
                self.data = apiresponse.json()

                ## -- Check for a valid nonempty response --
                assert self.data, f"No data found for {self.coin}."
                self.storejson(self.data, os.path.join(utils.getdirs(), f"data/{self.coin}_data.json")) if storejson else None

        except Exception as e:
            print(f"Error retrieving data for {self.coin}: {e}")


    def validate(self):
        if self.coin not in ["bitcoin", "ethereum", "both"]:
            raise ValueError("Invalid coin name. Please choose either 'bitcoin', 'ethereum' or 'both'.")
        
        print("Data validated successfully!")


    ## -- Return a dictionary for the urls for price data --
    def get_data_urldict(self):

        urls = {
            "bitcoin": "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=90&interval=daily",
            "ethereum": "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=90&interval=daily"
        }

        return urls
    

    ## -- Store the data in dedicated JSON file --
    def storejson(self, data, filename):

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Data stored in {filename}")


if __name__ == "__main__":
     
     os.system("CLS")

     print("Example run: ")
     c = cryptodata("both")