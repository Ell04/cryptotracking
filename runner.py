import analysis
import data
import utils
import os
import time
import plothandler


if __name__ == "__main__":

    print("Welcome to the Cryptotracking Data Analysis Tool!")
    time.sleep(1)


    coin = input("Do you want to retrieve data for bitcoin, ethereum, both or none? ")
    print(f"You have chosen: {coin}")
    data.cryptodata(coin) if coin.lower() in ["bitcoin", "ethereum", "both"] else None

    bitcoindatapath = os.path.join(utils.getdirs(), "data/bitcoin_data.json")
    ethereumdatapath = os.path.join(utils.getdirs(), "data/ethereum_data.json")

    time.sleep(1)
    choice = input("Process anomalies and events for bitcoin or ethereum? (bitcoin/ethereum): ")

    datapath = bitcoindatapath if choice.lower() == "bitcoin" else ethereumdatapath if choice.lower() == "ethereum" else None
    print("None chosen, exiting...") if datapath is None else None

    priceanomalies, volumeanomalies, marketcapanomalies = analysis.anomaly_pattern_detection(str(datapath), coin=choice.lower())

    choice2 = input("Do you want to see the plots (opens web browser)? (yes/no): ")
    plothandler.run_server_with_browser() if choice2.lower() == "yes" else print("You can view the plots in the 'plots' directory.")