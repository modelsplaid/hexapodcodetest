import dash_core_components as dcc
import dash_html_components as html
import dash

app = dash.Dash()

app.layout = html.Div([
    dcc.Interval(id='interval1', interval=0.5 * 1000, n_intervals=10),
    html.H1(id='label1', children='')
])


@app.callback(dash.dependencies.Output('label1', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    return 'Intervals Passed: ' + str(n)

app.run_server(debug=False, port=8050)
