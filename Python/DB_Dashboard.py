from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State

import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps

#import CRUD.py for username authentication
import sys
sys.path.append("../src/")
from CRUD.py import AnimalShelter

###########################
# Data Manipulation / Model
###########################

# input for username and password
username = "accuser"
password = "SapwordS"

# uses validation from CRUD file 
shelter = AnimalShelter(username, password)

# read data frame
df = pd.DataFrame.from_records(shelter.readAll({}))

#########################
# Dashboard Layout / View
#########################

app = JupyterDash('SimpleExample')

#Grazioso Salvare’s logo
image_filename = 'src/Grazioso_Salvare_Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    #Header
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    #Unique Identifier
    html.Center(html.B(html.H3('By Morgana Parsons'))),
    #Customer Logo
    html.Center(html.Img(id='customer-image',src='data:image/png;base64,{}'.format(encoded_image.decode()),alt='Grazioso Salvare Logo')),

    html.Hr(),
    html.Div(

    #Dropdown menu for filtering
        html.Label("Filter Options"),
        dcc.Dropdown(
            id='filter-dropdown',
            options=[
                {'label': 'Water Rescue', 'value': 'water'},
                {'label': 'Mountain/Wilderness', 'value': 'outdoor'},
                {'label': 'Disaster/Individual Tracking', 'value': 'disaster'}
            ],
            multi=True,
            value='water'
            ),
        html.Label("Chart Filter Options"),
        dcc.Dropdown(
            id='pie-filter-dropdown',
            options=[
                {'label': 'Breed', 'value': 'breed'},
                {'label': 'Age', 'value': 'age'},
            ],
            multi=True,
            value='breed'
        ),
        ),
    html.Hr(),
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "breed": i, "outcome_subtype": i, "sex_upon_outcome": i, "age_upon_weeks": i, "location_lat": i, "location_long": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
#Set up the features for your interactive data table to make it user-friendly for your client
        style_as_list_view = True,
        fixed_rows={'headers': True},
        style_table={'height': '300px', 'overflowY': 'auto', 'overflowX': 'auto'},
        page_size=15,
        page_action='native',
        sort_action='native',
        sort_mode="multi",
        filter_action='native',
        column_selectable='single',
        selected_rows=[],

    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('filter-dropdown', 'value')])
def update_dashboard(value):
### filter options for data table queries
    if (value == "water"): #Water Rescue option
        df = pd.DataFrame(list(shelter.readAll({"$and": [
            {"sex_upon_outcome":"Intact Female"},
            {"age_upon_outcome_in_weeks":{"$gte": 26}},
            {"age_upon_outcome_in_weeks":{"$lte": 156}},
            {"$or": [
                {"breed": "Labrador Retriever Mix"},
                {"breed": "Chesapeake Bay Retriever"},
                {"breed": "Newfoundland"},
            ]}
        ]}
        )))
    elif (value == "outdoor"): #Mountain/Wilderness option
          df = pd.DataFrame(list(shelter.read({"$and": [
              {"sex_upon_outcome":"Intact Male"},
              {"age_upon_outcome_in_weeks": {"$gte": 26}},
              {"age_upon_outcome_in_weeks": {"$lte": 156}},
              {"$or": [
                  {"breed":"German Shepherd"},
                  {"breed":"Alaskan Malamute"},
                  {"breed":"Old English Sheepdog"},
                  {"breed":"Siberian Husky"},
                  {"breed":"Rottweiler"}
                ]},
            ]}
        )))

    elif (value == "disaster"): #Disaster/Individual Tracking option
        df = pd.DataFrame(list(shelter.read(
            {"$and": [
                {"sex_upon_outcome":"Intact Male"},
                {"age_upon_outcome_in_weeks": {"$gte": 20}},
                {"age_upon_outcome_in_weeks": {"$lte": 300}},
                {"$or": [
                    {"breed":"German Shepherd"},
                    {"breed":"Doberman Pinscher"},
                    {"breed":"Golden Retriever"},
                    {"breed":"Bloodhound"},
                    {"breed":"Rottweiler"}
                ]}
            ]}
        )))
    columns=[{"name": i, "id": i, "breed": i, "location_long": i, "location_lat": i, "age_upon_outcome_in_weeks": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
    return (data,columns)

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# Callback to update graph 
@app.callback(
    Output('graph-id', 'children'),
    [Input('datatable-id','data'),
     Input('datatable-id','columns'),
     Input('pie-filter-dropdown', 'value')]
)
def update_graphs(data, columns, value):
    df = pd.DataFrame(data, columns), #import DataFrame from Dash Data Table
    if (value=='breed'):
        values= df['breed'].value_counts(normalize=True), #establish values for Pie chart breed categorizing
        names= df['breed'],
    elif (value=='age'):
        values= df['age_upon_outcome_in_weeks'].value_counts(normalize=True), #establish values for Pie chart age categorizing
        names= df['age_upon_outcome_in_weeks'],
    
    #Pie Chart should show the percentage of each subject available in the specified query selection
    return [
        dcc.Graph(
            id = 'pie-chart',
            fig = px.pie(df, values=values, names=names, title="Percent Available")
        )
    ]

# Call back to update map with selected row data
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id','columns'),
     Input('datatable-id','selected_rows')]
)
def update_map(columns, selected_rows):
    #load posiitonal data from the selected row of the data table
    selected_row = [columns[i] for i in selected_rows]
    markers = selected_row["location_lat", "location_long"]
    return [ # Austin TX is at [30.75,-97.48], home of Grazioso Salvare
        dl.Map(style={'width': '600px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            dl.Marker(position=markers, children=[
                dl.Tooltip(dff.iloc[0,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[1,9])
                ])
            ])
        ])
]

app
