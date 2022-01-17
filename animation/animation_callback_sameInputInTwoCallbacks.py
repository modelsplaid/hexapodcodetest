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
PAPER_BG_COLOR = "white"
LEGENDS_BG_COLOR = "rgba(255, 255, 255, 0.5)"
LEGEND_FONT_COLOR = "#34495e"

data = [
        {'color': 'rgba(244,22,100,0.6)',
              'opacity': 0.9,
              'type': 'mesh3d',
              'x': [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0],
              'y': [0.0, 100.0, 100.0, 0.0, -100.0, -100.0, 0.0],
              'z': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        },
        {
        "line": {"color": BODY_COLOR, "opacity": 1, "width": BODY_OUTLINE_WIDTH},
        "name": "body",
        "showlegend": True,
        "type": "scatter3d",
        "uid": "1f821e07-2c02-4a64-8ce3-61ecfe2a91b6",
        "x": [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0],
        "y": [0.0, 100.0, 100.0, 0.0, -100.0, -100.0, 0.0],
        "z": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
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
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[  
            dcc.Interval(id='interval1', interval=1 * 1000, n_intervals=10),
            html.H1(id='label1', children=''),
            html.Div(className='eight columns div-for-charts bg-grey',
                    children=[
                    dcc.Graph(id='timeseries_graph', figure=HEXAPOD_FIGURE)
            ]),
            html.Button(id='submit-button-state', n_clicks=0, children='Submit'), 
            html.Div(id='output-state')                           
        ]
)

@app.callback(Output('output-state', 'children'),
    dash.dependencies.Input('interval1', 'n_intervals'))

def update_output(n_interval):
    print(" 777777 the n_interval: " +str(n_interval) )
    return " 777777 the n_interval: " +str(n_interval)

@app.callback(dash.dependencies.Output('timeseries_graph', 'figure'),
    [dash.dependencies.Input('submit-button-state', 'n_clicks'),
    dash.dependencies.Input('interval1', 'n_intervals')
    ])
def update_interval(n,n_interval):
    print("---n clicks: "+str(n) + " n_interval: " +str(n_interval) )

    if((n+n_interval)%2):
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
    else:
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 300.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [300.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]


    return HEXAPOD_FIGURE

'''
@app.callback(dash.dependencies.Output('timeseries_graph', 'figure'),[dash.dependencies.Input('submit-button-state', 'n_clicks')])
def update_interval(n):
    print("n clicks: "+str(n))

    if(n%2):
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
    else:
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 300.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [300.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]


    return HEXAPOD_FIGURE



@app.callback(dash.dependencies.Output('timeseries_graph', 'figure'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    print("++++In interval"+str(n))
    if(n%2):
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
    else:
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 300.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [300.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]

    return HEXAPOD_FIGURE

@app.callback(dash.dependencies.Input('interval1', 'n_intervals'))
def update_interval(n):
    print("----In NO OUTPUT interval"+str(n))
    if(n%2):
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
    else:
        HEXAPOD_FIGURE["data"][0]['x'] = [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 300.0]
        HEXAPOD_FIGURE["data"][1]['x'] = [300.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0]
'''
    


if __name__ == '__main__':
    app.run_server(debug=True)
