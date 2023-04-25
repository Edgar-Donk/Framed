import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patheffects import withSimplePatchShadow
import pandas as pd
import mplcursors

sns.set_style('darkgrid')
df = pd.read_csv("../csv/brewery.csv")
df['original_extract'] = pd.to_numeric(df['original_extract'], errors='coerce')
df = df.dropna(subset=['calorific_value'])

colour_pal = {'Imperial Stout': '#1a1a1a', 'German Red': '#e8000b', 'Winterbier':
    '#ff7f00', 'Land-Pils': '#a6cee3', 'Kellerbier': '#b15928', 'Winterbock':
    '#6a3d9a', 'Doppelbock': '#6a3d9a', 'Citrus Pale Ale': '#fb9a99', 'Pils': '#1f78b4'}

def show_hover_panel(get_text_func=None):
    cursor = mplcursors.cursor(
        hover=2,  # Transient
        annotation_kwargs=dict(
            bbox=dict(
                boxstyle="square,pad=0.5",
                facecolor="white", # colour_pal,
                edgecolor="#ddd",
                linewidth=0.5,
                path_effects=[withSimplePatchShadow(offset=(1.5, -1.5))],
            ),
            linespacing=1.5,
            arrowprops=None,
        ),
        highlight=True,
        highlight_kwargs=dict(linewidth=2),
    )

    if get_text_func:
        cursor.connect(
            event="add",
            func=lambda sel: sel.annotation.set_text(get_text_func(sel.index)),
        )

    return cursor

def on_add(index):
    item = df.iloc[index]
    parts = [
        f"Brewery: {item.brewery}",
        f"Beer Type: {item.beer_type}",
        f"Calorific Value: {item.calorific_value:,.0f}kJ/100ml",
        f"Alcohol: {item.alcohol:,.1f}% v/v",
        f"Original Extract: {item.original_extract:,.1f}°P"
    ]

    return "\n".join(parts)


g = sns.relplot(data=df, x='calorific_value', y='alcohol', hue='beer_type',
        palette=colour_pal)
g.set_axis_labels("Calorific Value kJ/100ml", "Alcohol % v/v", labelpad=10)
g.fig.suptitle("Alcohol v Calorific Value for Various Beers")
g.legend.set_title("Beer Type")
g.despine(trim=True)
show_hover_panel(on_add)
plt.show()