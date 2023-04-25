import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')
dfc = pd.read_pickle("../csv/beer_list_cont.pkl")

# reading the Alcohol strength, by volume and weight
sns.regplot(dfc, x='AbW%', y='AbV%')
plt.show()