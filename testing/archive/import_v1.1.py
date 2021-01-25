# imports all the files from a directory
#
# function: import_results(folder_path):
#
#     - folder path: a string
#
#     returns: a dictionary with the file names as keys and the modules as values
#

import inspect
from os import listdir

# create a function that imports all of the results in a folder

def import_results(folder_path = "/users/sean/kraken_api_project/tradingproject/testing"):
    # first get the contents of the folder
    # file_names = [] (not needed)
    results = {} # dictionary to store the results
    # loop through the list of files in the directory and find the ones we need to import
    for filename in listdir(folder_path):
        if filename.startswith('f20'):
            # file_names.append(filename) # store all the file names in a list (or just import them) (not needed)
            print("Attempting to import " + filename + "...")
            try: # try to import the files
                results[filename] = __import__(filename[0:11])
                print("...success")
            except: # error if you are unable to import one or more of the files
                print("Error trying to import " + filename)
    return results

# to call the function and store the results in a dictionary just do this:
#   all_the_data = import_results(folder_path)
# to access a specific event just do this:
#   all_the_data['filename'].eventname

