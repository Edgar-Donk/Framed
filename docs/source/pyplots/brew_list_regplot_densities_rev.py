import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')
dfc = pd.read_pickle("../csv/beer_list_cont.pkl")
dfc.loc[10, ['Wort Density kg/m³']] = [1048.37]
dfc.loc[10, ['Beer Density kg/m³']] = [1009.69]

# reading the wort and beer densities
sns.regplot(dfc, x='Wort Density kg/m³', y='Beer Density kg/m³')
plt.show()
#plt.savefig('../figures/brew_list_regplot_densities_rev.png')