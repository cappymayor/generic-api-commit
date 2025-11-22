import pandas as pd
import requests

url = "https://randomuser.me/api/?results=100"


def female():
    response = requests.get(url)
    data = response.json()
    data.keys() 
    results = data["results"]

    females = []
    for i in results:
     if i["gender"] =="female" and i["dob"]['age'] < 43 :
        females.append(i)

    data= pd.json_normalize(females)

    return data


dataframe = female()

print(dataframe)