############################
# GRAZIOSO SALVARE DASHBOARD
############################

__author__ = "Morgana Val"
__credits__ = ["Morgana Val", "Coursework: CS-340 Southern New Hampshire University"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Morgana Val"
__email__ = "morgana.val20@gmail.com"


################
# Requirements
################

import os
import base64
from jupyter_plotly_dash import JupyterDash
from dash import dash_table as dt, html, dcc
import dash_leaflet as dl
import plotly.express as px
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps, loads
from CRUDmodule import AnimalShelter # Import CRUD for database


###########################
# Data Manipulation / Model
###########################

# change for your username and password
username = "accuser"
password = "SapwordS"
shelter = AnimalShelter(username, password)

# load and process database records
df = pd.DataFrame.from_records(shelter.read({}))

#encode Grazioso Salvare’s logo image
image_filename = open('Grazioso_Salvare_Logo.png', 'rb')
encoded_image = base64.b64encode(image_filename.read())


#########################
# Dashboard Layout / View
#########################

app = JupyterDash("AnimalShelter")

app.layout = html.Div([

# Page Title and Header
    html.Div(
        children=[
            html.Center(
                html.B(
                    html.H1('Grazioso Salvare Dashboard') #Title
                )
            ),
            html.Center(
                html.B(
                    html.H3('By Morgana Parsons') #Unique Identifier for CS 340 course
                )
            ),
            html.Center(
                html.Img(id='customer-image',src='data:image/png;base64,{}' #Customer Logo
                    .format(encoded_image.decode()),alt='Grazioso Salvare Logo',style={'height':'10%', 'width':'10%'}
                )
            ),
        ]
    ),
    html.Hr(),

#Dropdown menu for query option filtering
    html.Div(
        children=[
            html.Label("Filter Options"),
            dcc.Dropdown(
                id='filter-dropdown',
                options=[
                    {'label': 'Water Rescue', 'value': 'water'},
                    {'label': 'Mountain/Wilderness', 'value': 'outdoor'},
                    {'label': 'Disaster/Individual Tracking', 'value': 'disaster'}
                ],
                multi=False,
                value='',
            )
        ]
    ),
    html.Hr(),

#Data Table
    html.Div(
        dt.DataTable(
            id='datatable',
            columns=[{"name": i, "id": i, "deletable": False, "selectable": True}
             for i in df.loc[:,['name',
                               'animal_id',
                               'location_long',
                               'location_lat',
                               'breed',
                               'age_upon_outcome_in_weeks',
                               'sex_upon_outcome'
                              ]]
            ],
            #data=df.to_dict('records'),
            style_as_list_view = True,
            fixed_rows={'headers': True},
            style_table={'height': '600px', 'overflowY': 'auto', 'overflowX': 'auto'},
            page_size=15,
            page_action='native',
            sort_action='native',
            sort_mode="multi",
            filter_action='native',
            column_selectable='single',
            row_selectable='single',
            selected_columns=[],
            selected_rows=[],
        )
    ),
    html.Br(),
    html.Hr(),

# Charts
    html.Div(className='row',style={'display' : 'flex'},
        children=[
            html.Div(
                id='graph',
                className='col s12 m6',
            ),
            html.Div(
                id='map',
                className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

# DROPDOWN MENU OPTIONS AND QUERY ALGOS
@app.callback(
    Output('datatable', 'data'),
    [Input('filter-dropdown', 'value')])
#     # if second output is needed
def update_dashboard(value):
    global df
    if (value == "water"): #Water Rescue option
        df = pd.DataFrame(list(shelter.read({"$and": [
                {"sex_upon_outcome":"Intact Female"},
                {"age_upon_outcome_in_weeks":{"$gte": 26}},
                {"age_upon_outcome_in_weeks":{"$lte": 156}},
                {"$or": [
                    {"breed": "Labrador Retriever Mix"},
                    {"breed": "Chesapeake Bay Retriever"},
                    {"breed": "Newfoundland"},
            ]}
        ]})))

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
          ]})))

    elif (value == "disaster"): #Disaster/Individual Tracking option
        df = pd.DataFrame(list(shelter.read({"$and": [
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
            ]})))

    data = dumps(df.to_dict('records'))

    return data

# SELECTED COLUMNS ALGO
@app.callback(
    Output('datatable', 'style_data_conditional'),
    [Input('datatable', 'selected_columns')])

def update_styles(selected_columns):
    return [{'if': { 'column_id': i }, 'background_color': '#D2F3FF'} for i in selected_columns]

# UPDATE GRAPH ALGO
@app.callback(
    Output('graph', 'children'),
    [Input('datatable','data'), Input('datatable-id','columns')])

def update_graphs(data, columns):
    df = pd.DataFrame.from_dict(data, columns) #import DataFrame from Dash Data Table
    values= df['breed'].value_counts(normalize=True) #establish values for Pie chart
    #Pie Chart should show the percentage of each breed of the breeds available in the specified query selection
    return [ dcc.Graph(
                id = 'pie-chart',
                fig = px.pie(df, values=values, names=df['breed'], title="Percent of Breeds Available"))]

# UPDATE MAP ALGO
@app.callback(
    Output('map', 'children'),
    [Input('datatable','data'), Input('datatable-id','columns')])

def update_map(data, columns):
    #load data frame with Dash Data Table
    dff = pd.DataFrame.from_dict(data, columns)
    #load posiitonal data from data frame to markers
    markers = [dl.Marker(position=(dff.loc['location_lat', 'location_long'] for i in dff.iterrows),
                                   children=[
                                       dl.Tooltip(dff.iloc[0,4]),
                                       dl.Popup([html.H1("Animal Name"),
                                                 html.P(dff.iloc[1,9])])
                                   ]
                        )
              ]
    # Austin TX is at [30.75,-97.48], home of Grazioso Salvare
    return [dl.Map(style={'width': '600px', 'height': '500px'}, center=[30.75,-97.48], zoom=10,
               children=[
            # Marker with tool tip and popup
                    dl.LayersControl(
                        [dl.BaseLayer(dl.TileLayer(id="base-layer-id")),] +
                        [dl.Overlay(dl.LayerGroup(markers), name="markers", checked=True)]
                    ),
               ])
           ]


app
