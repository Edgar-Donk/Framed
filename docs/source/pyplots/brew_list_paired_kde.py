import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')
dfc = pd.read_pickle("../csv/beer_list_cont.pkl")

# reading the original, total and apparent extracts
cols_to_plot = ['OE°P', 'TE°P', 'AE°P']
sns.pairplot(dfc[cols_to_plot], diag_kind='kde')
plt.show()
#plt.savefig('../figures/br_list_paired_kde.png')