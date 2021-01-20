import numpy
from sklearn.preprocessing import MinMaxScaler

def prepare_data(df, look_back=1):
    # returns 4 arrays
    #    trainX, trainY, testX, and testY

    numpy.random.seed(7) # set random seed
    dataset = df.values # move the data into a numpy array
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

    return trainX, trainY, testX, testY

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