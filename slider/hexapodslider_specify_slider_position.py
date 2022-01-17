# https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div
# https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input
import dash_daq

SLIDER_ANGLE_RESOLUTION = 1.5
UPDATE_MODE = "drag"
SLIDER_HANDLE_COLOR = "#2c3e50"
SLIDER_COLOR = "#8e44ad"
DARKMODE = False
SLIDER_THEME = {
    "dark": DARKMODE,
    "detail": "#ffffff",
    "primary": "#ffffff",
    "secondary": "#ffffff",
}

ALPHA_MAX_ANGLE = 90

handle_style_x0y0 = {
    "showCurrentValue": True,
    "color": SLIDER_HANDLE_COLOR,
    "label": "x0y0",
}
handle_style_x1y0 = {
    "showCurrentValue": True,
    "color": SLIDER_HANDLE_COLOR,
    "label": "x1y0",
}

handle_style_x0y1 = {
    "showCurrentValue": True,
    "color": SLIDER_HANDLE_COLOR,
    "label": "x0y1",
}

handle_style_x1y1 = {
    "showCurrentValue": True,
    "color": SLIDER_HANDLE_COLOR,
    "label": "x1y1",
}



### alpha daq
daq_slider_x0y0 = dash_daq.Slider(  # pylint: disable=not-callable
    id="widget-x0y0",
    min=-ALPHA_MAX_ANGLE,
    max=ALPHA_MAX_ANGLE,
    value=1.5,
    step=SLIDER_ANGLE_RESOLUTION,
    size=300,
    updatemode=UPDATE_MODE,
    handleLabel=handle_style_x0y0 ,
    color={"default": SLIDER_COLOR},
    theme=SLIDER_THEME,
)

### beta daq
daq_slider_x1y0 = dash_daq.Slider(  # pylint: disable=not-callable
    id="widget-x1y0",
    min=-ALPHA_MAX_ANGLE,
    max=ALPHA_MAX_ANGLE,
    value=1.5,
    step=SLIDER_ANGLE_RESOLUTION,
    size=300,
    updatemode=UPDATE_MODE,
    handleLabel=handle_style_x1y0 ,
    color={"default": SLIDER_COLOR},
    theme=SLIDER_THEME,
)

daq_slider_x0y1 = dash_daq.Slider(  # pylint: disable=not-callable
    id="widget-x0y1",
    min=-ALPHA_MAX_ANGLE,
    max=ALPHA_MAX_ANGLE,
    value=1.5,
    step=SLIDER_ANGLE_RESOLUTION,
    size=300,
    updatemode=UPDATE_MODE,
    handleLabel=handle_style_x0y1 ,
    color={"default": SLIDER_COLOR},
    theme=SLIDER_THEME,
)

daq_slider_x1y1 = dash_daq.Slider(  # pylint: disable=not-callable
    id="widget-x1y1",
    min=-ALPHA_MAX_ANGLE,
    max=ALPHA_MAX_ANGLE,
    value=1.5,
    step=SLIDER_ANGLE_RESOLUTION,
    size=300,
    updatemode=UPDATE_MODE,
    handleLabel=handle_style_x1y1 ,
    color={"default": SLIDER_COLOR},
    theme=SLIDER_THEME,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def make_section_type2(div1, div2):
    return html.Div(
        [
            #html.Div(div2, style={"width": "50%"}),
            html.Div(div1,style={'padding': '40px 10px'}),
            html.Div(div2,style={'padding': '10px 10px'}),

        ],
        style={"display": "block"},
    )

slider_pos_vertical1 = make_section_type2(daq_slider_x0y0 , daq_slider_x1y0 )
slider_pos_vertical2 = make_section_type2(daq_slider_x0y1 , daq_slider_x1y1 )

slider_mix = html.Div(
        [
            slider_pos_vertical1,
            slider_pos_vertical2 
        ],
        style={"display": "flex"},
    )

app.layout = html.Div([
    html.H1('Overview'),

    html.Div(id='header'),
    slider_mix,
    html.Div(id='slider-output-container')
])

if __name__ == '__main__':
    app.run_server(debug=True,port = 8061)

