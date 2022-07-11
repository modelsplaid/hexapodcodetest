# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    html.Div(id='output-state2')
])


@app.callback(Output('output-state', 'children'),Output('output-state2', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_output(n_clicks, input1, input2):
    # return u'''
    #     The Button has been pressed {} times,
    #     Input 1 is "{}",
    #     and Input 2 is "{}"
    # '''.format(n_clicks, input1, input2)
    print("Output('output-state', 'children'):")
    print(type(Output('output-state', 'children')))
    return "input1: "+str(input1) ,"input2: "+str(input2)


if __name__ == '__main__':
    app.run_server(debug=True)