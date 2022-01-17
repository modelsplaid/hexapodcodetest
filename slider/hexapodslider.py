import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input
import dash_daq

SLIDER_ANGLE_RESOLUTION = 1.5
UPDATE_MODE = "drag"
SLIDER_HANDLE_COLOR = "#2c3e50"
SLIDER_COLOR = "#8e44ad"
DARKMODE = True
SLIDER_THEME = {
    "dark": DARKMODE,
    "detail": "#ffffff",
    "primary": "#ffffff",
    "secondary": "#ffffff",
}

ALPHA_MAX_ANGLE = 90

handle_style = {
    "showCurrentValue": True,
    "color": SLIDER_HANDLE_COLOR,
    "label": "alpha",
}

### alpha daq
daq_slider = dash_daq.Slider(  # pylint: disable=not-callable
    id="widget-alpha",
    min=-ALPHA_MAX_ANGLE,
    max=ALPHA_MAX_ANGLE,
    value=1.5,
    step=SLIDER_ANGLE_RESOLUTION,
    size=300,
    updatemode=UPDATE_MODE,
    handleLabel=handle_style,
    color={"default": SLIDER_COLOR},
    theme=SLIDER_THEME,
)

### beta daq
daq_slider_beta = dash_daq.Slider(  # pylint: disable=not-callable
    id="widget-beta",
    min=-ALPHA_MAX_ANGLE,
    max=ALPHA_MAX_ANGLE,
    value=1.5,
    step=SLIDER_ANGLE_RESOLUTION,
    size=300,
    updatemode=UPDATE_MODE,
    handleLabel=handle_style,
    color={"default": SLIDER_COLOR},
    theme=SLIDER_THEME,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def make_section_type2(div1, div2):
    return html.Div(
        [
            html.Div(div1, style={"width": "50%"}),
            html.Div(div2, style={"width": "50%"}),
        ],
        style={"display": "flex"},
    )


app.layout = html.Div([
    daq_slider,
    daq_slider_beta,
    html.Div(id='slider-output-container')
])

if __name__ == '__main__':
    app.run_server(debug=True)

