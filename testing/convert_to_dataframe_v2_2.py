# convert_to_dataframe_v1.0.py
#
# takes the imported dictionary and converts the data into a pandas data frame
#

import inspect
from datetime import datetime
# import pandas if it doesn't already exist
all_local_variables = locals()
yes_no = 0
# check to see if variable "pd" exists
for key in list(all_local_variables): # had to wrap the dictionary in a list so we wouldn't get an error
    if key == "pd":
        yes_no = 1
if yes_no == 0:
    import pandas as pd


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
    
    return df








# What do we want the data frame to look like? What columes are we going to have?
#
#
#
# ID  DATE        WeekDay  Time         Error  ErrorInfo bid1  bid2  bid3  bid1v  bid2v  bid3v  ask1  ask2  ask3  ask1v  ask2v  ask3v 
# 0   2020_09_23  3        15_37_37     0      0         ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ...
# 1   2020_09_23  3        15_37_40     0      0         ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ...
# 2   2020_09_23  3        15_37_43     0      0         ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ...
# 3   ...         ...      ...          ...    ...       ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ... 
# 
#
#
# What do we have?
#
#   after import we have something like this: z['f2020_09_23.py'].d15_37_37['weekday']
#
#       z - Dictionary (all the files in a dict)
#       f2020_09_23.py - A dictionary Key which is a Module (a file)
#       d15_37_37 - Dictionary (an Event of time)
#       weekday - Dictionary Key which is one value in an Event