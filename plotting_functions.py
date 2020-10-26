#plotting functions
"""
Required imports:
    pandas as pd
    matplotlib.pyplot as plt
"""

def histogram(input_data, bin_no):
    pd.DataFrame.hist(input_data, column=1, bins=bin_no)
    plt.title('Histogram of Timeseries')
    plt.xlabel('Timeseries Values')
    plt.ylabel('Frequency')
    
    



