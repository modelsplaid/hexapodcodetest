import pickle 
import json
BODY_COLOR = "#8e44ad"
BODY_OUTLINE_WIDTH = 10
AXIS_ZERO_LINE_COLOR = "#ffa801"
GROUND_COLOR = "rgb(240, 240, 240)"
PAPER_BG_COLOR = "white"
LEGENDS_BG_COLOR = "rgba(255, 255, 255, 0.5)"
LEGEND_FONT_COLOR = "#34495e"


data = [
        {'color': 'rgba(244,22,100,0.6)',
              'opacity': 0.9,
              'type': 'mesh3d',
              'x': [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0],
              'y': [0.0, 100.0, 100.0, 0.0, -100.0, -100.0, 0.0],
              'z': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        },
        {
        "line": {"color": BODY_COLOR, "opacity": 1, "width": BODY_OUTLINE_WIDTH},
        "name": "body",
        "showlegend": True,
        "type": "scatter3d",
        "uid": "1f821e07-2c02-4a64-8ce3-61ecfe2a91b6",
        "x": [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0],
        "y": [0.0, 100.0, 100.0, 0.0, -100.0, -100.0, 0.0],
        "z": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
        }      
        ]



HEXAPOD_FIGURE = {
    "data": data,
    "layout": {
        "paper_bgcolor": PAPER_BG_COLOR,
         "hovermode": "closest",
        "legend": {
            "x": 0,
            "y": 0,
            "bgcolor": LEGENDS_BG_COLOR,
            "font": {"family": "courier", "size": 12, "color": LEGEND_FONT_COLOR},
        },
    }
}
with open('filename.pickle', 'wb') as handle:
    # pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(HEXAPOD_FIGURE,handle,protocol=pickle.HIGHEST_PROTOCOL)


with open('file.json', 'w') as handle:
    json.dump(HEXAPOD_FIGURE,handle)
