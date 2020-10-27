# Functions to import time series data.

# Importing packages.
import numpy as np
import pandas as pd
import os

# Create file_name string variable.
file_name = './data/test_timeseries.csv'
# Determine file extension, while ignoring name output using _.
_, extension = os.path.splitext(file_name)
print(extension)

imp = {
    ".csv": "pd.read_csv(file, delimiter=',')",

    ".txt": "pd.read_table(file)",

    ".xls": "pd.read_excel(file)"
}


def import_file(file):

    # Determine file extension, while ignoring file name output using _.
    _, extension = os.path.splitext(file)
    return eval(imp[extension])


data = import_file(file_name)
print(data)
