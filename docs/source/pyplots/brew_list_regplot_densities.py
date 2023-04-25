import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')
dfc = pd.read_pickle("../csv/beer_list_cont.pkl")

# reading the wort and beer densities
sns.regplot(dfc, x='Wort Density kg/m³', y='Beer Density kg/m³', ci=None)
plt.show()