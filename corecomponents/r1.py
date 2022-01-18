import dash_core_components as dcc
import dash

app = dash.Dash(__name__)

app.layout = dcc.RadioItems(
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value='MTL',
    labelStyle={'display': 'flex'} # display of flex to create a vertical list, or of inline-block for horizontal.
)

if __name__ == "__main__":
    app.run_server(debug=True)
