import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)



INPUT_LIST = [
        dcc.Input(
            id="input_{}".format(_),
            type="text",
            value=7,
            min=0,
            step=0.01,

        )
        for _ in ALLOWED_TYPES
    ]
INPUT_LIST[0].value =90
print(INPUT_LIST)
app.layout = html.Div(
    INPUT_LIST
    + [html.H1(id="out-all-types")]
)


@app.callback(Output("input_number", "value"), [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],)
def cb_render(*vals):
    global INPUT_LIST 
    INPUT_LIST[1].value = 80
    return 369


if __name__ == "__main__":
    app.run_server(debug=True)

