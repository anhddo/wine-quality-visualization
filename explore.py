#%%
import urllib.request as request
import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt
plt.style.use('dark_background')
#%%
request.urlretrieve('https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv', 'white.csv')
request.urlretrieve('https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv', 'red.csv')
#%%
df_white = pd.read_csv('white.csv', delimiter=';')
df_red = pd.read_csv('red.csv')
#%%
df_white.head()
#%%
ax = df_white.groupby('quality').count().plot(y='pH', kind='bar')
ax.get_legend().remove()
plt.ylabel('number of samples')
plt.savefig('count.png')

#%%
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)
table(ax, df_white.head())
plt.savefig('table.png')