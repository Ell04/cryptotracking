import json
import os

def dumpjson(data, filename):
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def getdirs():

    return os.getcwd()