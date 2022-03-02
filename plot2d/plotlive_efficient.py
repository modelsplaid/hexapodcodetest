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
import time
X = deque(maxlen = 10)
X.append(1)
  
Y = deque(maxlen = 10)
Y.append(1)

Z = deque(maxlen = 10)
Z.append(1)

W = deque(maxlen = 10)
W.append(1)
data3 = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
)

data_3plots = [
    {
        'mode': 'lines+markers', 'name': 'Scatter', 'x': [1], 'y': [1]
    },
    {
        'mode': 'lines+markers', 'name': 'Scatter', 'x': [1], 'y': [1]
    },
    {
        'mode': 'lines+markers', 'name': 'Scatter', 'x': [1], 'y': [1]
    }
]
print(data3)

app = dash.Dash(__name__)
  
app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = False),
        dcc.Interval(
            id = 'graph-update',
            interval = 50,
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
    Z.append( math.cos(n/10.0))	 
    W.append( math.cos(n/10.0)+1)	 
    #data = plotly.graph_objs.Scatter(
    #        x=list(X),
    #        y=list(Y),
    #        name='Scatter',
    #        mode= 'lines+markers'
    #)   
    #data2 = plotly.graph_objs.Scatter(
    #    x=list(X),
    #    y=list(Z),
    #    name='Scatter2',
    #    mode= 'lines+markers'
    #)
    time1 = time.time()
    for i in range(20):

        data_3plots[0]['x'] = list(X)
        data_3plots[0]['y'] = list(Y)
        data_3plots[1]['x'] = list(X)
        data_3plots[1]['y'] = list(Z)
        data_3plots[2]['x'] = list(X)
        data_3plots[2]['y'] = list(W)
    time2 = time.time()
    print("running time: " +str((time2-time1)*1000) )
    return {'data': data_3plots,
            'layout' : go.Layout(xaxis=dict(range=[min(X),min(X)+10]),yaxis = dict(range = [-2,2]),)}
            
  
if __name__ == '__main__':
    app.run_server(port = 8061,debug=True)
