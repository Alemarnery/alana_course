#!/usr/bin/env python
# coding: utf-8

# # `Dash` Workflow
# ### Import the fundamental libraries

# In[18]:


import pandas as pd
import getpass
import plotly.graph_objs as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import numpy as np
import warnings


# ### Import AlanaPy library

# In[2]:


import credentials as cr
import alanapy
alana_token = cr.alana_token_open
root_url = "https://apps.alana.tech/open"
root_url = "http://127.0.0.1:8000/local"
myapi = alanapy.Datasource(alana_token, root_url)


# ### Visuals function and Callback

# In[23]:


#%%capture --no-display
# Get list of wells


# # Ignore future warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)


wells = myapi.getWells().df

# Create Dash app
app = Dash(__name__)

# Define layout
app.layout = html.Div([
    html.Label('Select well:'),
    dcc.Dropdown(
        id='well-dropdown',
        options=[{'label': name, 'value': name} for name in wells['well_name']],
        value=wells['well_name'].iloc[0]
    ),
    html.Div([
        dcc.Graph(id='oil-rate'),
        dcc.Graph(id='water-rate'),
        dcc.Graph(id='oil-cum'),
        dcc.Graph(id='water-cum')
    ], style={'columnCount': 2})
])

# Define callback to update graphs based on selected well
@app.callback(
    [
        Output('oil-rate', 'figure'),
        Output('water-rate', 'figure'),
        Output('oil-cum', 'figure'),
        Output('water-cum', 'figure')
    ],
    [Input('well-dropdown', 'value')]
)
def update_graphs(selected_well):
    try:
        # print(selected_well)
        # Get monthly production data for selected well
        df = myapi.getMonthlyProduction(well_names=[selected_well]).df
        #print(df.head(5))
        # Convert date strings to datetime objects
        df['date'] = pd.to_datetime(df['date'])
    
        # Filter data to include only oil and water rates/cumulative
        oil_rate = df[df['oil_rate'].notnull()][['date', 'oil_rate']]
        water_rate = df[df['wat_rate'].notnull()][['date', 'wat_rate']]
        oil_cum = df[df['oil_cum'].notnull()][['date', 'oil_cum']]
        water_cum = df[df['wat_cum'].notnull()][['date', 'wat_cum']]
    
        # Create figures
        oil_rate_fig = go.Figure(
            go.Scatter(x=oil_rate['date'], y=oil_rate['oil_rate'], mode='lines', line=dict(color='green'))
        )
        oil_rate_fig.update_layout(title='Oil Rate')
        water_rate_fig = go.Figure(
            go.Scatter(x=water_rate['date'], y=water_rate['wat_rate'], mode='lines', line=dict(color='blue'))
        )
        water_rate_fig.update_layout(title='Water Rate')
    
        oil_cum_fig = go.Figure(
            go.Scatter(x=oil_cum['date'], y=oil_cum['oil_cum'], mode='lines+markers', line=dict(color='green', dash='dot'))
        )
        oil_cum_fig.update_layout(title='Oil Cumulative')
        water_cum_fig = go.Figure(
            go.Scatter(x=water_cum['date'], y=water_cum['wat_cum'], mode='lines+markers', line=dict(color='blue', dash='dot'))
        )
        water_cum_fig.update_layout(title='Water Cumulative')
    
        return oil_rate_fig, water_rate_fig, oil_cum_fig, water_cum_fig
    except:
        return "Error in well data", "Error in well data", "Error in well data", "Error in well data"

# Run app
if __name__ == '__main__':
    app.run(debug=False, port=9000)


# ![image.png](dash.png)

# In[ ]:




