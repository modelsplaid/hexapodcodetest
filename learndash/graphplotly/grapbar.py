#https://plotly.com/python/creating-and-updating-figures/#converting-graph-objects-to-dictionaries-and-json
#https://plotly.com/python/bar-charts/
import pandas as pd
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import plotly
import dash
import time 
import numpy as np
app = dash.Dash()


leg_force = pd.DataFrame({
  "legs": ["right-middle", "right-front", "left-middle", "left-front", "right-back", "left-back",
           "right-middle", "right-front", "left-middle", "left-front", "right-back", "left-back"
           ],

  "robots":["real", "real", "real", "real", "real", "real",
            "sim", "sim", "sim", "sim", "sim", "sim"],

  "forces":[20, 1, 3, 1, 3, 2,
            19, 5, 4, 3 , 3, 2,],
})


fig_leg = px.bar(leg_force, x="legs", y="forces",color="robots", barmode="stack")

fig = go.Figure()

for robots, group in leg_force.groupby("robots"):
    fig.add_trace(go.Bar(x=group["legs"], y=group["forces"], name=robots,
      hovertemplate="Contestant=%s<br>Fruit=%%{x}<br>Number Eaten=%%{y}<extra></extra>"% robots))
fig.update_yaxes(range=[0, 21])

app.layout = html.Div(
    [
        dcc.Graph(id="force-live-graph",figure=fig),
        dcc.Interval(
            id = 'graph-update-inter',
            interval = 300,
            n_intervals = 2
        ),                                    
    ]
)

@app.callback(
    Output('force-live-graph','figure'),
    [ Input('graph-update-inter', 'n_intervals'),Input('force-live-graph','figure') ]
)
def update_graph_scatter(n,fig):
    #print("graph: ",n)
    #print("fig: ",fig)
    #print(fig['data'][0]['name'])

    # leg_force = pd.DataFrame({
    #   "legs": ["right-middle", "right-front", "left-middle", "left-front", "right-back", "left-back",
    #           "right-middle", "right-front", "left-middle", "left-front", "right-back", "left-back"
    #           ],

    #   "robots":["real", "real", "real", "real", "real", "real",
    #             "sim", "sim", "sim", "sim", "sim", "sim"],

    #   "forces":[20, 1, 3, 1, 3, 2,
    #             19, 5, 4, 3 , 3, 2,],
    # })

    # leg_force["forces"] = np.random.randint(0, 21, size=12)

    # #fig_leg = px.bar(leg_force, x="legs", y="forces",color="robots", barmode="stack")

    # fig = go.Figure()

    # for robots, group in leg_force.groupby("robots"):
    #     fig.add_trace(go.Bar(x=group["legs"], y=group["forces"], name=robots,
    #       hovertemplate="Contestant=%s<br>Fruit=%%{x}<br>Number Eaten=%%{y}<extra></extra>"% robots))
    #print(fig['data'][0]['name'])


    fig['data'][0]["y"] = np.random.randint(0, 21, size=6)
    return fig
  


if __name__ == '__main__':
  print("main")
  app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

  print("quit")