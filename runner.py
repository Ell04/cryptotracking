import analysis
import data
import utils
import os
import plothandler
import questionary
from time import sleep
from llm_semantics import GeminiModel

def main():
    os.system("CLS")

    coin = questionary.select(
        "Which cryptocurrency would you like to track?",
        choices=["bitcoin", "ethereum", "both"]
    ).ask()

    sleep(2)

    compute_data = questionary.confirm(
        "Would you like to compute new data? (This will overwrite existing data)",
        default=False
    ).ask()

    sleep(2)

    data.cryptodata(coin) if compute_data else None

    if coin == "both":
        coin = questionary.select(
            "Which cryptocurrency would you like to analyse?",
            choices=["bitcoin", "ethereum"]
        ).ask()
    
    bitcoindatapath = os.path.join(utils.getdirs(), "data/bitcoin_data.json")
    ethereumdatapath = os.path.join(utils.getdirs(), "data/ethereum_data.json")

    ## -- Anomalies are already printed and or shown, no need to use the variables here, but just to contextualise the returns
    datapath = bitcoindatapath if coin == "bitcoin" else ethereumdatapath if coin == "ethereum" else None
    priceanomalies, volumeanomalies, marketcapanomalies = analysis.anomaly_pattern_detection(str(datapath), coin=coin)

    sleep(2)

    visualse = questionary.confirm(
        "Would you like to visualise the anomalies?",
        default=False
        ).ask()
    
    sleep(2)
    
    plothandler.run_server_with_browser() if visualse else print("You can view the plots in the 'plots' directory.")

    get_semantics = questionary.confirm(
        "Would you like to get semantic reasoning behind the anomalies? (Induces LLM calls)",
        default=False
    ).ask()

    GeminiModel.run_semantics() if get_semantics else print("Semantic analysis by LLMs not requested.")

    sleep(2)

    print("--" * 20)

    
    

main()