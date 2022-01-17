import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import json
# Load data
df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

# Initialize the app
app = dash.Dash(__name__)

# reference https://plotly.com/python/figure-structure/

fig3 = ({
    'data': [{'hovertemplate': 'x=%{x}<br>y=%{y}<extra></extra>',
              'legendgroup': '',
              'line': {'color': '#636efa', 'dash': 'solid'},
              'marker': {'symbol': 'circle'},
              'mode': 'lines',
              'name': '',
              'orientation': 'v',
              'showlegend': False,
              'type': 'scatter',
              'x': ['a', 'b', 'c'] ,
              'xaxis': 'x',
              'y': [10, 3, 2],
              'yaxis': 'y'}],
    'layout': {'height': 625,
               'legend': {'tracegroupgap': 0},
               'template': '...',
               'title': {'text': 'sample figure'},
               'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'x'}},
               'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'y'}}}
})


fig = px.line(
    x=["a","b","c"], y=[1,3,2], 
    title="sample figure", height=625
)
print(fig)

fig2 ={
  "data": [
    {
      "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>",
      "legendgroup": "",
      "line": {
        "color": "#636efa",
        "dash": "solid"
      },
      "mode": "lines",
      "name": "",
      "orientation": "v",
      "showlegend": 0,
      "x": [
        "a",
        "b",
        "c"
      ],
      "xaxis": "x",
      "y": [
        3,
        1,
        9
      ],
      "yaxis": "y",
      "type": "scatter"
    }
  ]}

app.layout = html.Div(
    children=[   
            html.Div(className='eight columns div-for-charts bg-grey',
                    children=[
                    dcc.Graph(id='timeseries', figure=fig3,config={'displayModeBar': False}, animate=True)
            ])
                            
        ]

)

if __name__ == '__main__':
    app.run_server(debug=True)
