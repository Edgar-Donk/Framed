import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")
# Load the example tips dataset
tips = sns.load_dataset("tips")

sns.boxplot(data=tips, x='day', y='total_bill')

plt.show()
#plt.savefig('../figures/tips_box.png')