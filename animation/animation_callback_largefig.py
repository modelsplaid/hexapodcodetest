import plotly.graph_objects as go
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import dash
import time
from dash.dependencies import Input, Output, State

BODY_COLOR = "#8e44ad"
BODY_OUTLINE_WIDTH = 10
AXIS_ZERO_LINE_COLOR = "#ffa801"
GROUND_COLOR = "rgb(240, 240, 240)"
PAPER_BG_COLOR = "rgb(240, 240, 0)"
H1_BG_COLOR = "rgb(0, 240, 240)"
LEGENDS_BG_COLOR = "rgba(255, 255, 255, 0.5)"
LEGEND_FONT_COLOR = "#34495e"

data = [
        {'color': 'rgba(244,22,100,0.6)',
              'opacity': 0.9,
              'x': [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0],
              'y': [0.0, 100.0, 100.0, 0.0, -100.0, -100.0, 0.0],

        },
        {
        "line": {"color": BODY_COLOR, "opacity": 1, "width": BODY_OUTLINE_WIDTH},
        "name": "body",
        "showlegend": True,
        "type": "scatter3d",
        "uid": "1f821e07-2c02-4a64-8ce3-61ecfe2a91b6",
        "x": [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0],
        "y": [0.0, 100.0, 100.0, 0.0, -100.0, -100.0, 0.0],
        }      
        ]



HEXAPOD_FIGURE = {
    "data": data,
    "layout": {
        "paper_bgcolor": PAPER_BG_COLOR,
         "hovermode": "closest",
        "legend": {
            "x": 0,
            "y": 0,
            "bgcolor": LEGENDS_BG_COLOR,
            "font": {"family": "courier", "size": 12, "color": LEGEND_FONT_COLOR},
        },
    }
}

HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 300.0]
HEXAPOD_FIGURE["data"][1]['x'] = [300.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]

print(HEXAPOD_FIGURE["data"][0]['x'])
print(HEXAPOD_FIGURE["data"][1]['x'])

sidebar_layout = html.Div(
    id='sidebar1',
    children=[
            html.Button(id='submit-button-state', n_clicks=0, children='Submit',style={"padding": "2%"}),                            
            html.Button(id='activate_interval1', n_clicks=0, children='activate interval1',style={"padding": "2%"}),   
            html.Button(id='activate_interval2', n_clicks=0, children='activate interval2',style={"padding": "2%"}),   
            html.Button(id='activate_interval3', n_clicks=0, children='activate interval3',style={"padding": "2%"}),   
            html.Button(id='activate_interval4', n_clicks=0, children='activate interval4',style={"padding": "2%"}),   
            html.Button(id='activate_interval5', n_clicks=0, children='activate interval5',style={"padding": "2%"}),                         
        ],
    style={"display": "flex","flex-direction": "column","justify-content":"center","width": "10%","height": "100%"} 
        
)

app = dash.Dash(__name__)
app.layout = html.Div(
    children=[  
            html.H1(id='label1', children='Hello Dash'),
            sidebar_layout,
            html.Div(className='eight columns div-for-charts bg-grey',
                    children=[
                    dcc.Graph(id='timeseries_graph', figure=HEXAPOD_FIGURE)
            ]),
        ],style={"display": "flex","flex-direction": "column","justify-content":"center","padding": "2%"}               
        
)




if __name__ == '__main__':
    app.run_server(debug=True)
