# -*- coding: utf-8 -*-
"""Plotly Dashboard.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LzcNsRICEG84V7pZDjiYKJrgeoA_CGwy
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

pip install dash

pip install dash-core-components dash-html-components

data=pd.read_csv('netflix.csv')
data.head()

data.info()
data.describe()

# Checking for missing values
missing = data.isnull().sum()
print("Missing Values:")
print(missing)

data['director'].fillna('Unknown', inplace=True)
data['cast'].fillna('Unknown', inplace=True)
data['country'].fillna('Unknown', inplace=True)

# Convert date-related columns to datetime format
data['date_added'] = pd.to_datetime(data['date_added'])

# Remove any leading/trailing whitespaces in categorical columns
data['type'] = data['type'].str.strip()
data['country'] = data['country'].str.strip()
data['rating'] = data['rating'].str.strip()

# After Cleaning
print("Cleaned Dataset:")
print(data.head())

# Movie Genres barplot
plt.figure(figsize=(6, 6))
genre_counts = data['listed_in'].value_counts().head(10)
sns.barplot(x=genre_counts.values, y=genre_counts.index)
plt.xlabel('Number of Titles')
plt.ylabel('Genre')
plt.title('Top 10 Movie Genres')
plt.show()

#Release Years lineplot
plt.figure(figsize=(6, 6))
release_year_counts = data['release_year'].value_counts().sort_index()
sns.lineplot(x=release_year_counts.index, y=release_year_counts.values)
plt.xlabel('Release Year')
plt.ylabel('Number of Titles')
plt.title('Distribution of Release Years')
plt.xticks(rotation=45)
plt.show()

# Ratings barplot
plt.figure(figsize=(6, 6))
rating_counts = data['rating'].value_counts()
sns.barplot(x=rating_counts.values, y=rating_counts.index)
plt.xlabel('Number of Titles')
plt.ylabel('Rating')
plt.title('Distribution of Ratings')
plt.show()

#scatter plot
scatter_plot = px.scatter(data, x='release_year', y='duration', color='type', hover_data=['title'])
scatter_plot.update_layout(title='Release Year vs. Duration', xaxis_title='Release Year', yaxis_title='Duration')
scatter_plot.show()

#barchart
bar_chart = px.bar(data['country'].value_counts().head(10), orientation='h')
bar_chart.update_layout(title='Top 10 Countries with Most Titles', xaxis_title='Number of Titles', yaxis_title='Country')
bar_chart.show()

#pie chart
pie_chart = px.pie(data['rating'].value_counts(), names=data['rating'].value_counts().index)
pie_chart.update_layout(title='Distribution of Ratings')
pie_chart.show()

import dash
import dash_core_components as dcc
import dash_html_components as html

# Create a Dash application
app = dash.Dash(__name__)

# Define the style and layout of the application
app.layout = html.Div(
    style={'font-family': 'Arial, sans-serif', 'margin': '50px'},
    children=[
        html.H1(
            children="Netflix Movies and TV Shows",
            style={'text-align': 'center', 'font-size': '32px', 'margin-bottom': '40px'}
        ),
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'},
            children=[
                dcc.Graph(
                    id='scatter-plot',
                    figure=px.scatter(data, x='release_year', y='duration', color='type', hover_data=['title']),
                    style={'width': '48%', 'height': '400px', 'margin': '10px'}
                ),
                dcc.Graph(
                    id='bar-chart',
                    figure=px.bar(data['country'].value_counts().head(10), orientation='h'),
                    style={'width': '48%', 'height': '400px', 'margin': '10px'}
                ),
                dcc.Graph(
                    id='line-plot',
                    figure=px.line(data['release_year'].value_counts().sort_index()),
                    style={'width': '48%', 'height': '400px', 'margin': '10px'}
                ),
                dcc.Graph(
                    id='pie-chart',
                    figure=px.pie(data['rating'].value_counts()),
                    style={'width': '48%', 'height': '400px', 'margin': '10px'}
                )
            ]
        ),
        html.Div(
            style={'text-align': 'center', 'margin-top': '40px'},
            children=[
                html.Label(
                    "Filter by Type",
                    style={'font-size': '20px'}
                ),
                dcc.Dropdown(
                    id='type-dropdown',
                    options=[
                        {'label': 'Movie', 'value': 'Movie'},
                        {'label': 'TV Show', 'value': 'TV Show'}
                    ],
                    value='Movie',
                    style={'width': '200px', 'margin-top': '10px'}
                )
            ]
        )
    ]
)

# Add interactivity
@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    Output(component_id='bar-chart', component_property='figure'),
    Input(component_id='type-dropdown', component_property='value')
)
def update_plots(selected_type):
    filtered_data = data[data['type'] == selected_type]

    scatter_plot = px.scatter(filtered_data, x='release_year', y='duration', color='type', hover_data=['title'])
    bar_chart = px.bar(filtered_data['country'].value_counts().head(10), orientation='h')

    scatter_plot.update_layout(title='Release Year vs. Duration', xaxis_title='Release Year', yaxis_title='Duration')
    bar_chart.update_layout(title='Top 10 Countries with Most Titles', xaxis_title='Number of Titles', yaxis_title='Country')

    return scatter_plot, bar_chart

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)