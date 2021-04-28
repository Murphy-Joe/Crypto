import requests
import json
from pprint import pprint
import csv
from datetime import datetime
import re

###################################################

""" with open ("eth.csv", "w") as eth_file:
    writer = csv.writer(eth_file)
    writer.writerow(["Date", "Time", "DateTime", "Avg", "Volume"]) """

###################################################

# only used if not getting last date from file
last_date = "2021-02-11T16:00:00Z"

# file that keeps track of last date received from api call
with open('lastdate.json') as f:
    last_date = json.load(f)

# can be out of date, just to get loop rolling
dtime = datetime(2021,2,1,0,0,0)

headers = {"content-type": "application/json"}
url = "https://data.messari.io/api/v1/assets/ETH/metrics/price/time-series"

counter = 0

while dtime < datetime.now() and counter < 5:

    # dynamic params date
    params = {"after":last_date, "timestamp-format":"rfc3339", "format":"json"}
    r = requests.get(url, headers=headers, params=params)
    eth = json.loads(r.text)

    # create date variable for next api call
    hourlies = eth['data']['values']
    last_date = hourlies[-1][0] # 2021-02-01T00:00:00Z
    print(last_date)
    with open('lastdate.json', 'w') as json_file:
        json.dump(last_date, json_file)

    # datetime obj and counter for loop condition
    dt_parts = re.split(r'\D+', last_date)
    a, b, c, d, e, f = [int(i) for i in dt_parts if i]
    dtime = datetime(a, b, c, d, e, f)
    counter +=1

    # get data 
    for hour in hourlies[1:]:
        dt = hour[0][:10]
        hr = hour[0][11:19]
        high = hour[2]
        low = hour[3]
        avg = (high+low)/2
        vol = hour[5]
        #print(hour[0])
        with open ("eth.csv", "a") as eth_file:
            writer = csv.writer(eth_file)
            writer.writerow([dt, hr, dt+' '+hr, avg, vol])
    
    




