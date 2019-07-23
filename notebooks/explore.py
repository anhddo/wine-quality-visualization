# %%
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('seaborn')
plt.rcParams['savefig.facecolor'] = 'white'
mpl.rcParams['savefig.dpi'] = 200

df_white = pd.read_csv('data/white.csv', delimiter=';')
df_red = pd.read_csv('data/red.csv', delimiter=';')

def convert_class(x): return 'good' if x >= 7 else 'bad'

df_white['class'] = df_white['quality'].apply(convert_class)
df_red['class'] = df_red['quality'].apply(convert_class)
df_white['type'] = 'white'
df_red['type'] = 'red'
# %%
df_comb = pd.concat([df_white, df_red])[['type', 'class']]
df_comb['count'] = 0
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
                (p.get_x()+0.25, p.get_height()+30))
plt.savefig('img/range-class.png')

# %%
sns.countplot(x='class', data=df_white)
plt.savefig('img/class.png')

# %%
# df_comb.plot.bar()
mpl.style.use('ggplot')
df_comb.groupby(['type', 'class']).count().unstack().plot.bar(stacked=True)
plt.legend(['Bad', 'Good'])
plt.xticks([0, 1], ['Red', 'White'], rotation='horizontal')
plt.xlabel('Wine type')
plt.title('Good and bad wine')
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
        v = df_corr.values[i, j]
        patches.append(Circle((i, n-j-1), abs(0.5*v), fc=cmap(v)))
# df_corr.values
ax.add_collection(PatchCollection(patches, match_original=True))
plt.colorbar(scalable_map, ax=ax)
plt.ylim(-1, n)
plt.xlim(-1, n)
plt.savefig('img/corr.png', bbox_inches='tight')
# %%
sns.pairplot(data=df_white[['class', 'alcohol']],  hue='class')
plt.legend()
# %%
ax = plt.gca()
sns.distplot(df_white[df_white['class'] == 'bad']['alcohol'], ax=ax)
sns.distplot(df_white[df_white['class'] == 'good']['alcohol'], ax=ax)
plt.legend(['bad', 'good'])
plt.title('Good feature.')
plt.savefig('img/good_ftr.png')
# %%
ax = plt.gca()
sns.distplot(df_white[df_white['class'] == 'bad']['citric acid'], ax=ax)
sns.distplot(df_white[df_white['class'] == 'good']['citric acid'], ax=ax)
plt.legend(['bad', 'good'])
plt.title('Bad feature')
plt.savefig('img/bad_ftr.png')
# %%
clf = DecisionTreeClassifier(max_depth=3)
x = df_red.drop(['class', 'type', 'quality'], axis=1)
y = [1 if i == 'good' else 0 for i in df_red['class']]
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)
clf.fit(x_train, y_train)
f1_score(y_test, clf.predict(x_test))

#%%
from sklearn import tree
tree.plot_tree(clf)

#%%
x_train.shape
x.columns[10]
x.columns[9]

#%%
# dir(clf.tree_)
from sklearn.tree.export import _MPLTreeExporter
# _MPLTreeExporter._make_tree()
clf.tree_.children_left
