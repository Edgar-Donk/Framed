import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')
dfc = pd.read_pickle("../csv/beer_list_cont.pkl")
dfc.loc[10, ['Wort Density kg/m³']] = [1048.37]
dfc.loc[10, ['Beer Density kg/m³']] = [1009.69]

# reading the wort and beer densities
cols_to_plot = ['Wort Density kg/m³', 'Beer Density kg/m³']
sns.pairplot(dfc[cols_to_plot], diag_kind='kde', kind='reg',
            plot_kws={'line_kws':{'color':'red'}})
plt.show()