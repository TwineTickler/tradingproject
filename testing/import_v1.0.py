import inspect
import some_results

# get the length of all the methods in the results
inspect_results = inspect.getmembers(some_results)
type(inspect_results) # this is a list
len(inspect_results) # get the length of the list
inspect_results[8] # this is where the dictionaries should start
# you can loop through the list and find all the dictionaries
# you can also get a name for each of the dictionaries
numberofdictionariesinfile = 0
dic_names = []
for x in inspect_results:
    if str(type(x[1])) == "<class 'dict'>":
        dic_names.append(x[0])
        numberofdictionariesinfile += 1 # make a count of all the dictionaries
numberofdictionariesinfile # here are the total number of dictionaries
# you can also just find the number of dict's by using the len(dic_names)
len(dic_names) # this will also give you the number of dictionaries
# PROBLEM: the first element in the list[0][1] is a dict! so We'll need to exclude it from the list
for x in inspect_results:
    if str(type(x[1])) == "<class 'dict'>" and x[0] != "__builtins__":
        dic_names.append(x[0])
# Now you have a list of all the dict names in the current file. yay
# Now, how do we loop through all the data in all the dicts?
# We can use the eval method to make python interpret strings as variables
s = ""
for dict_title in dic_names:
    s = "some_results." + dict_title
    eval(s) # shows entire dict
    eval(s).keys() # shows keys
    eval(s).values() # shows values
    eval(s)['error'] # shows value of error (0 or 1)
# This is how we can check for any errors:
s = ""
good_connections = 0
bad_connections = 0
for dic_name in dic_names:
    s = "some_results." + dic_name
    if eval(s)['error'] == 0:
        good_connections += 1
    else:
        bad_connections += 1
# how can we check how many files are in the results folder and what the names of the files are so we can import them?
files_to_import = []
from os import listdir
path = 'users/sean/kraken_api_project/tradingproject/testing'
listdir(path) # this will give you a list of everything in the path directory
for filename in listdir(path):
    if filename.startswith('f20'): # this will be true if the file starts with 'f20'
        files_to_import.append(filename) # import this file
        # this is how to import the file (module)
        new_module = __import__(filename[0:11])
        
new_module.d15_37_37 # how to call the dictionary from the file
# next we need to name the module with the filename



# get current working directory
os.getcwd()

# import one of the dicts from the file
test_set = some_results.d15_37_37

print(type(test_set))


