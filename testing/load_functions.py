import inspect
from os import listdir
import os
from datetime import datetime
import pandas as pd
import numpy
from sklearn.preprocessing import MinMaxScaler

# import numpy
import matplotlib.pyplot as plt
# import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
# from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# create a function that imports all of the results in a folder

def import_results(folder_path = "/users/sean/kraken_api_project/tradingproject/results/"):
    # need to change directories to the results folder!
    current_dir = os.getcwd() # get the current dir
    os.chdir(folder_path)
    # first get the contents of the folder
    # file_names = [] (not needed)
    results = {} # dictionary to store the results
    # loop through the list of files in the directory and find the ones we need to import
    for filename in listdir(folder_path):
        if filename.startswith('f20'):
            # file_names.append(filename) # store all the file names in a list (or just import them) (not needed)
            print("Attempting to import " + filename + "...", end='') # end='' should print without a new line
            try: # try to import the files
                results[filename] = __import__(filename[0:11])
                print("...success")
            except Exception as e: # error if you are unable to import one or more of the files
                print("Error trying to import " + filename)
                print(e)

    os.chdir(current_dir) # change the dir back to original 
    return results

def convert_to_dataframe(all_data):
    event_names = []
    # iterate through the keys in the dict (aka, file names)
    for key in all_data:
        # print out all the values in the dict (all the modules/files)
        print(all_data[key])
        # for each value in the dictionary (module/file), find all the dictionaries (events) and put them in a list called "event_names"
        # we need to store them as tuples with the name of the file as well,
        # so then we will have a list of tuples of all the events, and all the file names
        inspect_results = inspect.getmembers(all_data[key])
        for x in inspect_results:
            if str(type(x[1])) == "<class 'dict'>" and x[0] != "__builtins__":
                event_names.append((key,x[0]))
    # now we have a list called "event_names" that has ALL of the File names and Event names that correspond to them
    
    # we should be able to see one event like this now:
    # all_data['f2020_09_23.py'].d15_37_37['weekday']
    #
    # s = ""
    # s = "all_data['" + event_names[0][0] + "']." + event_names[0][1]
    # eval(s)

    # now lets convert the data into a list of a list so we can import it into a DataFrame easily
    # the list will look like this:
    #    all_data_list = [['2020_09_23', 3, '15_37_37', 0 , ...],['2020_09_23', 3, '15_37_40', 0, ...], ...]
    # then we should be able to create the DF like this:
    #    df = pd.DataFrame(all_data_list, columns = ['Date', 'WeekDay', 'CurrentTime', ...])

    # loop through the event_names and create a list of all the strings to evaluate into variables
    # in other words, a list of each event
    all_data_list = []
    c = 0 # counter for troubleshooting:
    last_good_time = "" # keep record of the last good time stamp in the loop for errors
    for x in event_names:
        c = c+1
        s = "all_data['" + x[0] + "']." + x[1] # string of a dictionary event
        d = eval(s)
        current_date_as_string = str(x[0][1:11])
        current_date = int((current_date_as_string[0:4] + current_date_as_string[5:7] + current_date_as_string[8:]))
        if int(d['error']) == 1: # if there is an error, write a different entry
            all_data_list.append([None, True, last_good_time, None, None, None, None, None, None, None, None, None, None, None, None])
        else: # no error, write a successful entry
            build_datetime = datetime(int(current_date_as_string[0:4]), int(current_date_as_string[5:7]), int(current_date_as_string[8:]), int(d['currenttime'][0:2]), int(d['currenttime'][3:5]), int(d['currenttime'][6:]))
            last_good_time = int((d['currenttime'][0:2] + d['currenttime'][3:5] + d['currenttime'][6:]))
            all_data_list.append([build_datetime, False, None, float(d['bid1']), float(d['bid2']), float(d['bid3']), float(d['bid1vol']), float(d['bid2vol']), float(d['bid3vol']), float(d['ask1']), float(d['ask2']), float(d['ask3']), float(d['ask1vol']), float(d['ask2vol']), float(d['ask3vol'])])
    
    # create the data frame from all_data_list
    df = pd.DataFrame(all_data_list, columns = ['Datetime', 'Error', 'ErrorInfo', 'bid1', 'bid2', 'bid3', 'bid1v', 'bid2v', 'bid3v', 'ask1', 'ask2', 'ask3', 'ask1v', 'ask2v', 'ask3v'])

    # sort the new df by datetime and re-index it
    df = df.sort_values(by="Datetime", ascending=True)
    df = df.reset_index(drop=True)

    # remove all errors
    df = df[df["Error"] == False]
    # remove all columns except bid1
    df = df['bid1']

    # print out the plot of the data
    plt.plot(df)

    # print out the description of the data
    df.describe()

    return df

def prepare_data(df, look_back=1):
    # returns 4 arrays
    #    trainX, trainY, testX, and testY

    numpy.random.seed(7) # set random seed
    dataset = df.values # move the data into a numpy array
    dataset = dataset.reshape(-1, 1) # reshape the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset) # normalize the dataset
    # spit the data in to train and test data sets. 
    # This will use the Index to keep everything in time properly
    train_size = int(len(dataset) * 0.67)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
    print(len(train), len(test))

    #reshape into X=t and Y=t+1
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    # The LSTM expects the input data to be a specific array structure in the form of: 
    # [samples, time steps, features]
    # currently we have: [samples, features]
    # I think what we have to do is just add a increment value for the "time steps" part of the array

    #reshape input to be [samples, time steps, features]
    trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    return trainX, trainY, testX, testY, scaler

# convert an array of values into a dataset matrix
# This should give us something like:
    # look_back will be the number of time events to use to predict the next time event (default 1)
    # x will be the price at a given event (t) and Y will be the price at the next event (t + 1)
    # (later we might want to change this to say.. 60? I don't know)

def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return numpy.array(dataX), numpy.array(dataY)