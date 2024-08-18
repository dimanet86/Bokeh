from bokeh.plotting import figure, show
from bokeh.palettes import HighContrast3
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10
import pandas as pd
import numpy as np

data = pd.read_csv("Titanic-Dataset.csv")
def age_group(x): 
    if x >= 0 and x <= 12:
        return 'Child'
    elif x > 12 and x <= 19:
        return 'Teenager'
    elif x > 19 and x <= 35:
        return 'Young'
    elif x > 35 and x <= 65:
        return 'Adult'
    elif x > 65:
        return 'Senior'

survival_df = data[data['Age'].notna()].copy() # Let's take rows WITH values, and skip rows missing age

# Creating Age Group column
survival_df['AgeGroup'] = survival_df['Age'].apply(age_group)
# Survival rate: as Survived is Bernoulli RV, let's calculate mean by groups
survived_grouped_mean = survival_df.groupby('AgeGroup')['Survived'].mean()

# Creating column SurvivalRate
survival_df['SurvivalRate'] = survival_df['AgeGroup'].apply(lambda x: survived_grouped_mean.loc[x])

horizontal = list(survived_grouped_mean.index)
vertical = list(survived_grouped_mean)

# Create a ColumnDataSource
source = ColumnDataSource(data=dict(
    x=horizontal,
    y=vertical
))

# Create the figure
p = figure(x_range=horizontal, height=400, title="Survival Rates by Age Group",
           toolbar_location=None, tools="")

# Add the vertical bars
p.vbar(x='x', top='y', width=0.9, source=source)

# Configure the tooltips
hover = HoverTool(tooltips=[
    ("Age Group", "@x"),
    ("Survival Rate", "@y{0.00}")  # Display survival rate with two decimals
])

# Add the HoverTool to the figure
p.add_tools(hover)
# Customize the plot
p.xgrid.grid_line_color = None
p.y_range.start = 0

# Display the plot
show(p)

"""
Class and Gender: Create a grouped bar chart to compare survival rates across 
different classes (1st, 2nd, 3rd) and genders (male, female).
"""

# Checking if columns in question have missing values
data[data['Pclass'].isna()]
data[data['Sex'].isna()]

# Preparing data
sex_class_data = data[['Sex', 'Pclass', 'Survived']].copy() 
grouped = sex_class_data.groupby(['Sex', 'Pclass'])['Survived'].mean()
sex_class_data['SurvivalRate'] = sex_class_data[['Sex', 'Pclass']].apply(lambda x: grouped.loc[(x['Sex'], x['Pclass'])], axis=1)

gender = list(sex_class_data['Sex'].unique())
pclass = list(sex_class_data['Pclass'].unique())

data_to_plot = {
    'gender': gender,
    1: [],
    2: [],
    3: []
}

for i in pclass:
    for j in gender:
        data_to_plot[int(i)].append(float(grouped.loc[(j, i)]))

fruits = data_to_plot['gender']
years = ["1", "2", ""]

data2 = {'fruits' : data_to_plot['gender'],
        '1'   : data_to_plot[1],
        '2'   : data_to_plot[2],
        '3'   : data_to_plot[3]}

p = figure(x_range=fruits, height=250, title="Survival Rate By Gender Grouped By Class",
           toolbar_location=None, tools="hover", tooltips="$name @fruits: @$name")

p.vbar_stack(years, x='fruits', width=0.9, color=HighContrast3, source=data2,
             legend_label=years)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)

# Fare vs Survival Scatter Plot
# Map the class to colors

data['Pclass'] = data['Pclass'].astype(str)

# Define the unique classes and colors
class_labels = ['1', '2', '3']
colors = Category10[3]

# Create a ColumnDataSource
source = ColumnDataSource(data)

# Create the plot
p = figure(title="Fare vs. Survival by Class",
           x_axis_label="Fare",
           y_axis_label="Survived",
           tools="pan,wheel_zoom,box_zoom,reset")

# Add the scatter plot with factor_cmap
p.scatter(x='Fare', y='Survived', source=source, size=10,
          color=factor_cmap('Pclass', palette=colors, factors=class_labels),
          legend_field='Pclass')

# Customize the legend
p.legend.title = 'Class'
p.legend.location = 'top_right'

# Show the plot
show(p)