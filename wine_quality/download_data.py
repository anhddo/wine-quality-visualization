#%%
import shutil
import urllib.request as request
import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt
from os import path
import os
#%%
if path.exists('data'):
    shutil.rmtree('data',    ignore_errors=True)
os.makedirs('data')
request.urlretrieve('https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv', 'data/white.csv')
request.urlretrieve('https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv', 'data/red.csv')
# print(os.path.abspath(__file__))
# print(__file__)
