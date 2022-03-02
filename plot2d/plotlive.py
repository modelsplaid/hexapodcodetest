#https://www.geeksforgeeks.org/plot-live-graphs-using-python-dash-and-plotly/
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import math  
X = deque(maxlen = 10)
X.append(1)
  
Y = deque(maxlen = 10)
Y.append(1)

Z = deque(maxlen = 10)
Z.append(1)
  
app = dash.Dash(__name__)
  
app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = False),
        dcc.Interval(
            id = 'graph-update',
            interval = 100,
            n_intervals = 100
        ),
    ]
)
  
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)
  
def update_graph_scatter(n):
    X.append(X[-1]+1)
    Y.append( math.sin(n/10.0))	  	
    Z.append( math.cos(n/10.0))	  	
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
    )

    data2 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Z),
            name='Scatter2',
            mode= 'lines+markers'
    )

  
    return {'data': [data,data2],
            'layout' : go.Layout(xaxis=dict(range=[min(X),min(X)+10]),yaxis = dict(range = [-2,2]),)}
            
  
if __name__ == '__main__':
    app.run_server(port = 8061,debug=True)
