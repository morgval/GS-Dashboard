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

# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
import sys
sys.path.append("../src/")
from CRUD.py import AnimalShelter





###########################
# Data Manipulation / Model
###########################
# change for your username and password and CRUD Python module name
username = "accuser"
password = "SapwordS"
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object 
df = pd.DataFrame.from_records(shelter.readAll({}))



#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

#Add in Grazioso Salvare’s logo
image_filename = 'src/Grazioso_Salvare_Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    #Unique Identifier
    html.Center(html.B(html.H3('By Morgana Parsons'))),
    #Customer Logo
    html.Center(html.Img(id='customer-image',src='data:image/png;base64,{}'.format(encoded_image.decode()),alt='Grazioso Salvare Logo')),
    
    html.Hr(),
    html.Div(
        
#Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.
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
            value='MTL'
            )
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
        selected_columns=[],
        
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
### Add code to filter interactive data table with MongoDB queries
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

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id','data'),
     Input('datatable-id','columns')])
def update_graphs(data, columns):
    # add code for chart of your choice (e.g. pie chart)
    df = pd.DataFrame(data, columns) #import DataFrame from Dash Data Table
    values= df['breed'].value_counts(normalize=True) #establish values for Pie chart
    #Pie Chart should show the percentage of each breed of the breeds available in the specified query selection
    return [
        dcc.Graph(
            id = 'pie-chart',
            fig = px.pie(df, values=values, names=df['breed'], title="Percent of Breeds Available") 
        )    
    ]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id','data'),
     Input('datatable-id','columns')])
    
    
#Add in the code for your geolocation chart
#If you completed the Module Six Assignment, you can copy in the code you created here.
        

def update_map(data, columns):
    dff = pd.DataFrame.from_dict(data, columns) #load data frame with Dash Data Table
    markers = dff["location_lat", "location_long"] #load posiitonal data from data frame
    # Austin TX is at [30.75,-97.48], home of Grazioso Salvare
    return [
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
