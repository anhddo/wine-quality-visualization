# %%
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('ggplot')
plt.rcParams['savefig.facecolor'] = 'white'
mpl.rcParams['savefig.dpi'] = 200

# %%
df_white = pd.read_csv('data/white.csv', delimiter=';')
df_red = pd.read_csv('data/red.csv', delimiter=';')
# %%
n_white, n_red = df_white.shape[0], df_red.shape[0]
data_count = {'name': ['red', 'white'], 'count': [n_red, n_white]}
sns.barplot(x='name', y='count', data=data_count)
plt.savefig('img/count.png')
# %%
# df_white.groupby('quality').count().plot(x='quality', y='pH', kind='bar')
ax = sns.countplot(x='quality', data=df_white)
for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()),
                (p.get_x()+0.15, p.get_height()+1))
plt.savefig('img/range-class.png')
# %%


def convert_class(x): return 'good' if x >= 7 else 'bad'


df_white['class'] = df_white['quality'].apply(convert_class)
df_red['class'] = df_red['quality'].apply(convert_class)
df_white['type'] = 'white'
df_red['type'] = 'red'
# %%
sns.countplot(x='class', data=df_white)
plt.savefig('img/class.png')
# %%
df_comb = pd.concat([df_white, df_red])[['type', 'class']]
df_comb['count'] = 0
# %%
# df_comb.plot.bar()
df_comb.groupby(['type', 'class']).count().unstack().plot.bar(stacked=True)
plt.legend(['Bad', 'Good'])
plt.savefig('img/good-bad-type.png')
# %%
# %%
df_corr = df_white.drop(['type', 'class'], axis=1).corr()
n = len(df_corr.columns)
plt.yticks(np.arange(n), df_corr.columns[::-1])
plt.xticks(np.arange(n), df_corr.columns, rotation='vertical')
ax = plt.gca()
ax.xaxis.tick_top()
ax.set_aspect('equal')
plt.grid(False)
for i in range(n+1):
    plt.axvline(i-0.5, -0.5, n)
    plt.axhline(i-0.5, -0.5, n)
# plt.axvline()

cmap = mpl.colors.Colormap('mymap')
cmap.set_under("#2d3561")
cmap.set_over('#f3826f')
cmap = plt.get_cmap('viridis', 12)
scalable_map = mpl.cm.ScalarMappable(mpl.colors.Normalize(-1, 1), cmap)
patches = []
for i in (range(n)):
    for j in (range(n)):
        if i == j:
            continue
        v=df_corr.values[i, j]
        patches.append(Circle((i, n-j-1), abs(0.5*v), fc=cmap(v)))
# df_corr.values
ax.add_collection(PatchCollection(patches, match_original=True))
plt.colorbar(scalable_map, ax=ax)
plt.ylim(-1, n)
plt.xlim(-1, n)
plt.savefig('img/corr.png', bbox_inches='tight')
# %%
