# convert_to_series
#
# converts the imported dictionary and converts the data in to a pandas series
#

import inspect

# import pandas if it doesn't already exist
all_local_variables = locals()
yes_no = 0
# check to see if variable "pd" exists
for key in all_local_variables:
    if key == "pd":
        yes_no = 1
if yes_no == 0:
    import pandas as pd

##########   DONE IMPORTING   ##########

def convert_to_series(dict):
    pass
