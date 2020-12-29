# convert_to_dataframe_v1.0.py
#
# takes the imported dictionary and converts the data into a pandas data frame
#

# import pandas if it doesn't already exist
all_local_variables = locals()
yes_no = 0
# check to see if variable "pd" exists
for key in all_local_variables:
    if key == "pd":
        yes_no = 1
if yes_no == 0:
    import pandas as pd

def convert_to_dataframe(dict):
    # iterate through the keys in the dict (aka, file names)
    for k in dict:
        print(k)



# What do we want the data frame to look like? What columes are we going to have?
#
#
#
# ID  DATE        WeekDay  CurrentTime  Error  bid1  bid2  bid3  bid1v  bid2v  bid3v  ask1  ask2  ask3  ask1v  ask2v  ask3v 
# 0   2020_09_23  3        15_37_37     0      ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ...
# 1   2020_09_23  3        15_37_40     0      ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ...
# 2   2020_09_23  3        15_37_43     0      ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ...
# 3   ...         ...      ...          ...    ...   ...   ...   ...    ...    ...    ...   ...   ...   ...    ...    ...
# 
#
#
