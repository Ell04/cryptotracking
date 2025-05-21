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

        ## -- Get the filename to store the data based on user's local machine directory and validate --
        self.filename = os.path.join(utils.getdirs(), f"data/{self.coin}_data.json")
        self.validate()

        try:
            
            ## -- From https://docs.coingecko.com/v3.0.1/reference/coins-id-market-chart --
            print(f"Retrieving data for {self.coin}...")

            ## -- Get URL from the dictionary --
            url = self.urls[self.coin]

            ## -- Set headers for the request --
            headers = {"accept": "application/json"}

            ## -- Make the API request and get data as JSON --
            apiresponse = requests.get(url, headers=headers, timeout=10)
            self.data = apiresponse.json()

            ## -- Check for a valid response --
            if not self.data:
                raise ValueError("No data found for the specified coin.")

            print(f"Data retrieved successfully for {self.coin}.")

            ## -- Dump JSON if boolean storejson is true in class --
            self.storejson(self.data, self.filename) if storejson else None

        except Exception as e:
            print(f"Error retrieving data: {e}")


    def validate(self):
        if self.coin not in ["bitcoin", "ethereum"]:
            raise ValueError("Invalid coin name. Please choose either 'bitcoin' or 'ethereum'.")
        
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
     
     print("Example run: ")
     c = cryptodata("bitcoin")