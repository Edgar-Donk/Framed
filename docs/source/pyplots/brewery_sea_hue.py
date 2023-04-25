import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style('darkgrid')
df = pd.read_csv("../csv/brewery.csv")

sns.scatterplot(data=df, x='calorific_value', y='alcohol', hue='beer_type')

plt.show()