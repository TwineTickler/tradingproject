# TODO:
#

import krakenex
import pprint
import time
import datetime

kraken = krakenex.API()
counter = 0
# this will set how long the script will run for:
iterations = 100000000 # how many times would you like to check the price?
# 100,000,000 one hundered million is about 3 years

while counter < iterations:
    if counter != 0: # if this is not the first time through the loop then wait 3 seconds
        time.sleep(1)
        print('.')
        time.sleep(1)
        print('.')
        time.sleep(1)
    # staticly set the time to a variable so that it doesn't change for any of the time calculations
    timenow = datetime.datetime.utcnow()
    currenttime = str(timenow)[11:19]
    currenttime = currenttime.replace(":","_",2) # python is picky about : in variable names so replace with _
    # get the current weekday
    year = str(timenow)[0:4]
    month = str(timenow)[5:7]
    day = str(timenow)[8:10]
    weekday = datetime.datetime(int(year),int(month),int(day)).weekday()
    # lets store all the price data in a file, that is named by date
    currentfilename = "../results/f" + str(timenow)[0:10] + ".py"
    currentfilename = currentfilename.replace("-","_",2) # python will not import this file unless it doesn't have - and starts with a letter
    # create the file if it doesn't already exist
    try:
        open(currentfilename,"x")
        # print("new file created")
    except:
        pass
    # add the open function to a variable f with the correct filename
    f = open(currentfilename,"a")
    # f.write("content \n") # write to the file using the open function
    try:
        currentbook = kraken.query_public('Depth', {'pair': 'XXBTZUSD', 'count': '3'})
        # if error is not empty then do something else:
        if currentbook['error'] != []:
            f.write("d" + currenttime + "={'error':'1'}\n")
            print('There is an error')
        # pprint.pprint(currentbook['result'])
        # print("\n")
        bid1 = currentbook['result']['XXBTZUSD']['bids'][0][0]
        bid2 = currentbook['result']['XXBTZUSD']['bids'][1][0]
        bid3 = currentbook['result']['XXBTZUSD']['bids'][2][0]
        ask1 = currentbook['result']['XXBTZUSD']['asks'][0][0]
        ask2 = currentbook['result']['XXBTZUSD']['asks'][1][0]
        ask3 = currentbook['result']['XXBTZUSD']['asks'][2][0]
        bid1volume = currentbook['result']['XXBTZUSD']['bids'][0][1]
        bid2volume = currentbook['result']['XXBTZUSD']['bids'][1][1]
        bid3volume = currentbook['result']['XXBTZUSD']['bids'][2][1]
        ask1volume = currentbook['result']['XXBTZUSD']['asks'][0][1]
        ask2volume = currentbook['result']['XXBTZUSD']['asks'][1][1]
        ask3volume = currentbook['result']['XXBTZUSD']['asks'][2][1]
        f.write("d" + currenttime + "={'weekday':'" + str(weekday) + "','error':'0','currenttime':'" + currenttime + "','bid1':'" + bid1 + "','bid2':'" + bid2 + "','bid3':'" + bid3 + "','bid1vol':'" + bid1volume + "','bid2vol':'" + bid2volume + "','bid3vol':'" + bid3volume + "','ask1':'" + ask1 + "','ask2':'" + ask2 + "','ask3':'" + ask3 + "','ask1vol':'" + ask1volume + "','ask2vol':'" + ask2volume + "','ask3vol':'" + ask3volume + "'}\n")
        print("time: " + currenttime + " --- bid 1: " + bid1 + " --- ask 1: " + ask1)
    except: # except HTTPError as e:
        f.write("d" + currenttime + "={'error':'1'}\n")
        print("error at: " + currenttime) # print(str(e))
    f.close() # close the file
    counter = counter + 1