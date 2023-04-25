import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='darkgrid')
# superimpose box and strip plots

tips = sns.load_dataset("tips")
# jitter places points apart in same data set, dodge separates different categories
sns.stripplot(x="day", y="total_bill", hue="smoker",
data=tips, jitter=True,
palette="Set2", dodge=True,linewidth=1,edgecolor='gray')

# Get the ax object to use later.
ax = sns.boxplot(x="day", y="total_bill", hue="smoker",
data=tips,palette="Set2",fliersize=0)

# Get the handles and labels. For this example it'll be 2 tuples
# of length 4 each.
handles, labels = ax.get_legend_handles_labels()

# When creating the legend, only use the first two elements
# to effectively remove the last two.
l = plt.legend(handles[0:2], labels[0:2], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.show()