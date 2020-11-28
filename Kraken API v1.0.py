import krakenex
import pprint
import time
import datetime

kraken = krakenex.API()
counter = 0

# lets store all the price data in a file, that is named by date
currentfilename = str(datetime.datetime.today())[0:10] + ".txt"
# create the file if it doesn't already exist
try:
    open(currentfilename,"x")
    # print("new file created")
except:
    pass
# add the open function to a variable f with the correct filename
f = open(currentfilename,"a")
f.write("content \n") # write to the file using the open function
f.close() # close the file

while counter < 0:
    try:
        currentbook = kraken.query_public('Depth', {'pair': 'XXBTZUSD', 'count': '1'})
        # if error is not empty then do something else:
        if currentbook['error'] != []:
            print('There is an error')
        # pprint.pprint(currentbook['result'])
        # print("\n")
        currentbid = currentbook['result']['XXBTZUSD']['bids'][0][0]
        currentask = currentbook['result']['XXBTZUSD']['asks'][0][0]
        currentbidvolume = currentbook['result']['XXBTZUSD']['bids'][0][1]
        currentaskvolume = currentbook['result']['XXBTZUSD']['asks'][0][1]
        currentbidtime = currentbook['result']['XXBTZUSD']['bids'][0][2]
        currentasktime = currentbook['result']['XXBTZUSD']['asks'][0][2]
        print("current bid is: " + currentbid)
        print("current bid volume is: " + currentbidvolume)
        print('current bid time is:' + str(currentbidtime))
        print("current ask is: " + currentask)
        print("current ask volume is: " + currentaskvolume)
        print('current ask time is: ' + str(currentasktime))
        print("\n")
    except HTTPError as e:
        print(str(e))
    time.sleep(3)
    counter = counter + 1