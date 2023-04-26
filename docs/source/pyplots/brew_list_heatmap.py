import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')
dfc = pd.read_pickle("../csv/beer_list_cont.pkl")
dfch = dfc[['OE°P', 'AbV%', 'FP°C', 'TMD°C']]
print(dfch)
corr = dfch.corr()
sns.heatmap(corr)

plt.show()
#plt.savefig('../figures/brew_list_heatmap.png')