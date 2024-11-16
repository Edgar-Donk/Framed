import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='darkgrid')
# Load the example tips dataset
tips = sns.load_dataset('tips')

sns.catplot(data=tips, x="time", y="total_bill", hue="sex", col="day", aspect=.5)

plt.show()
#plt.savefig('../figures/tips_catplot.png')