import requests
import os
import utils

import analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# TODO: Use google AI


load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

def gptrequest(priceanomalies, volumeanomalies, marketcapanomalies, coin):

    client = OpenAI(api_key=OPENAI_KEY)

    with open("prompt.txt", "r") as file:
        prompt = file.read()

    for priceanomaly in tqdm(priceanomalies):
        prompt = prompt.format(date=priceanomaly, coin=coin)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = response.choices[0].message.content

        filename = f"data/responses/{coin}_price_anomaly_response_{priceanomaly}.txt"
        with open(filename, "w") as file:
            file.write(response_text)
        
        print(f"Response for price anomaly on {priceanomaly} saved to {filename}")

    for volumeanomaly in tqdm(volumeanomalies):
        prompt = prompt.format(date=volumeanomaly)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = response.choices[0].message.content

        filename = f"data/responses/{coin}_volume_anomaly_response_{volumeanomaly}.txt"
        with open(filename, "w") as file:
            file.write(response_text)
        
        print(f"Response for volume anomaly on {volumeanomaly} saved to {filename}")

    for marketcapanomaly in tqdm(marketcapanomalies):
        prompt = prompt.format(date=marketcapanomaly[0])

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = response.choices[0].message.content

        filename = f"data/responses/{coin}_marketcap_anomaly_response_{marketcapanomaly}.txt"
        with open(filename, "w") as file:
            file.write(response_text)
        
        print(f"Response for market cap anomaly on {marketcapanomaly} saved to {filename}")



if __name__ == "__main__":
    os.system("CLS")

    bitcoindatapath = os.path.join(utils.getdirs(), "data/bitcoin_data.json")
    ethereumdatapath = os.path.join(utils.getdirs(), "data/ethereum_data.json")
    choice = input("Process anomalies and events for bitcoin or ethereum? (bitcoin/ethereum): ")

    datapath = bitcoindatapath if choice.lower() == "bitcoin" else ethereumdatapath if choice.lower() == "ethereum" else None
    print("None chosen, exiting...") if datapath is None else None


    priceanomalies, volumeanomalies, marketcapanomalies = analysis.anomaly_pattern_detection(str(datapath), coin=choice.lower())
    gptrequest(priceanomalies, volumeanomalies, marketcapanomalies, choice.lower())