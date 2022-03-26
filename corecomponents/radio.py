import dash_core_components as dcc
import dash
import dash_html_components as html
app = dash.Dash(__name__)

app.layout = html.Div([dcc.RadioItems(
                        id = 'r1',
                        options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montréal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        value='MTL',
                        labelStyle={'display': 'flex'} # display of flex to create a vertical list, or of inline-block for horizontal.
                        ),
                        html.Div(id='output-container-button',
                        children='Enter a value and press submit')
])



@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('r1', 'value')])
def update_output(value):
    return 'The input value was "{}" '.format(
        value
    )


if __name__ == "__main__":
    app.run_server(debug=True)
