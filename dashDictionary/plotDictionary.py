import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import json
HEXAPOD_FIGURE = {
 
    "layout": {       
        "hovermode": "closest",
        "legend": {
            "x": 0,
            "y": 0,
        },
        "margin": {"b": 20, "l": 10, "r": 10, "t": 20},
        "scene": {
            "aspectmode": "manual",
            "aspectratio": {"x": 1, "y": 1, "z": 1},
            "camera": {
                "center": {
                    "x": 0.0348603742736399,
                    "y": 0.16963779995083,
                    "z": -0.394903376555686,
                },
                "eye": {
                    "x": 0.193913968006015,
                    "y": 0.45997575676993,
                    "z": -0.111568465000231,
                },
                "up": {"x": 0, "y": 0, "z": 1},
            },
            "xaxis": {
                "nticks": 1,
                "range": [-600, 600],              
                "showbackground": False,
            },
            "yaxis": {
                "nticks": 1,
                "range": [-600, 600],             
                "showbackground": False,
            },
            "zaxis": {
                "nticks": 1,
                "range": [-600, -10],        
                "showbackground": True,        
            },
        },
    },
}


app = dash.Dash(__name__)

df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

dict_main = {'df1': df1, 'df2': df2}
data = list(dict_main.keys())
channels = dict_main[data[0]]

app.layout = html.Div([
        dcc.Graph(id='Main-Graph',
            #figure=go.Figure(
            #    data=[go.Scatter(x=data, y=channels)])
            figure = HEXAPOD_FIGURE
            ),

        html.Div([
            dcc.Dropdown(
                id='data-dropdown',
                options=[{'label': label, 'value': label} for label in data],
                value=list(dict_main.keys())[0],
                multi=False,
                searchable=False)],
            style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='x-axis-dropdown',
                multi=False)],
            style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='y-axis-dropdown',
                multi=False)],
            style={'width': '33%', 'display': 'inline-block'}),        
])

# @app.callback(
#     [dash.dependencies.Output('x-axis-dropdown', 'options'),
#      dash.dependencies.Output('y-axis-dropdown', 'options')],
#     [dash.dependencies.Input('data-dropdown', 'value')]
# )
# def update_date_dropdown(selected):
#     if selected:
#         fields = [{'label': i, 'value': i} for i in dict_main[selected]]
#         return [fields, fields]

# @app.callback(
#     dash.dependencies.Output('Main-Graph', 'figure'),
#     [dash.dependencies.Input('data-dropdown', 'value'),
#      dash.dependencies.Input('x-axis-dropdown', 'value'),
#      dash.dependencies.Input('y-axis-dropdown', 'value')],
#     [dash.dependencies.State('Main-Graph', 'figure')])
# def updateGraph(df_name, x_field, y_field, data):
#     source = data['data']
#     df = dict_main[df_name]

#     if x_field and y_field and x_field in df.columns and y_field in df.columns:
#         new_source = [{'x': df[x_field].tolist(), 'y': df[y_field].tolist()}]
#         source = new_source
#     return {
#         'data': source,
#         'layout': data['layout']
#     }

if __name__ == '__main__':
    app.run_server(debug=True)
