import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import time
from threading import Thread
import plotly.express as px
import plotly.graph_objects as go

import plotly.express as px
import plotly.graph_objects as go

leg_force = pd.DataFrame({
  "legs": ["right-middle", "right-front", "left-middle", "left-front", "right-back", "left-back",
           "right-middle", "right-front", "left-middle", "left-front", "right-back", "left-back"
           ],

  "robots":["real", "real", "real", "real", "real", "real",
            "sim", "sim", "sim", "sim", "sim", "sim"],

  "forces":[20, 1, 3, 1, 3, 2,
            19, 5, 4, 3 , 3, 2,],
})


# Function to update forces
def update_forces():
      while True:
        leg_force["forces"] = np.random.randint(1, 21, leg_force.shape[0])
        time.sleep(1)

# Start the thread to update forces
thread = Thread(target=update_forces)
thread.daemon = True
thread.start()

app = dash.Dash(__name__)

app.layout = html.Div([
  dcc.Graph(id='live-update-graph'),
  dcc.Interval(
    id='interval-component',
    interval=1*1000,  # in milliseconds
    n_intervals=0
  )
])


fig_leg = px.bar(leg_force, x="legs", y="forces",color="robots", barmode="group")

fig = go.Figure()
for robots, group in leg_force.groupby("robots"):
    fig.add_trace(go.Bar(x=group["legs"], y=group["forces"], name=robots,
      hovertemplate="Contestant=%s<br>Fruit=%%{x}<br>Number Eaten=%%{y}<extra></extra>"% robots))


app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=fig_leg)])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

@app.callback(Output('live-update-graph', 'figure'),
        Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    print("n:", n)
    fig_leg = px.bar(leg_force, x="legs", y="forces", color="robots", barmode="group")
    return fig_leg

