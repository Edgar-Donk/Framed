import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='darkgrid')
# superimpose box and strip plots

tips = sns.load_dataset("tips")
# jitter places points apart in same data set, dodge separates different categories
sns.violinplot(x="day", y="total_bill", data=tips, color="0.8")
sns.stripplot(x="day", y="total_bill", data=tips, jitter=True, zorder=1, hue='day')

plt.show()