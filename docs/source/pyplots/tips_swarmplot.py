import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")
# Load the example tips dataset
tips = sns.load_dataset("tips")

sns.swarmplot(data=tips, x="total_bill", y="day", hue="size", palette="deep")

plt.show()