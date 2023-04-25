import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='darkgrid')

tips = sns.load_dataset('tips')

sns.violinplot(x = 'day',y = 'tip',  data = tips, hue = 'sex', split = True, palette = 'rainbow')

plt.show()