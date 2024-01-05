import  json 
import  numpy as np

from copy                       import deepcopy
from typing                     import List

from custom_type.axis_type      import AxisType
from custom_type.bot_vecs_type  import BotVecArr
from custom_type.car_sqs_type   import CarSqsType
from custom_type.hexagon_type   import HexgnPtsType
from custom_type.valv_pump_type import ValvPumpActType

BODY_MESH_COLR       = "#ff6348"
BODY_MESH_OPAC       = 0.3
BODY_COLR            = "#FC427B"
BODY_OUTLINE_WIDTH   = 12
COB_COLR             = "#32ff7e"
COB_SIZE             = 14
HEAD_SIZE            = 14
LEG_COLR             = "rgba(238, 90, 36, 0.9)" 
LEG_COLR_VP_OFF      = "rgba(248, 100, 46, 0.7)"  

LEG_OUTLINE_WIDTH    = 10
LEGENDS_BG_COLR      = "rgba(44, 62, 80, 0.8)"
AXIS_ZERO_LINE_COLR  = "#222f3e"
PAPER_BG_COLR        = "#0a3d62"
GROUND_COLR          = "rgb(240, 240, 240)"
LEGEND_FONT_COLR     = "#079992"
SUPRT_POLY_MESH_COLR = "#3c6382"
SUPRT_POLY_MESH_OPAC = 0.2
HEAD_COLR            = "#8e44ad"

FIG_DATA = [
    { #0
        "name"      : "body mesh",
        "showlegend": True,
        "type"      : "mesh3d",
        "opacity"   : BODY_MESH_OPAC,
        "color"     : BODY_MESH_COLR,
        "uid"       : "1f821e07-2c02-4a64-8ce3-61ecfe2a91b6",
        "x"         : [100.0, 100.0, -100.0, -100.0, -100.0, 100.0 , 100.0],
        "y"         : [0.0  , 100.0, 100.0 , 0.0   , -100.0, -100.0,  0.0 ],
        "z"         : [100.0, 100.0, 100.0 , 100.0 , 100.0 , 100.0 , 100.0],
    },
    {  #1
        "line"      : {"color": BODY_COLR, "opacity": 1.0, "width": BODY_OUTLINE_WIDTH},
        "name"      : "body",
        "showlegend": True,
        "type"      : "scatter3d",
        "uid"       : "1f821e07-2c02-4a64-8ce3-61ecfe2a91b6",
        "x"         : [100.0, 100.0, -100.0, -100.0, -100.0, 100.0, 100.0],
        "y"         : [0.0, 100.0, 100.0, 0.0, -100.0, -100.0, 0.0],
        "z"         : [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
    },
    { #2
        "marker"    : {"color": COB_COLR, "opacity": 0.6, "size": COB_SIZE},
        "mode"      : "markers",
        "name"      : "cob",
        "type"      : "scatter3d",
        "uid"       : "a819d0e4-ddaa-476b-b3e4-48fd766e749c",
        "x"         : [0.0],
        "y"         : [0.0],
        "z"         : [100.0],
    },
    { #3
        "marker"    : {"color": BODY_COLR, "opacity": 1.0, "size": HEAD_SIZE},
        "mode"      : "markers",
        "name"      : "head",
        "type"      : "scatter3d",
        "uid"       : "508caa99-c538-4cb6-b022-fbbb31c2350b",
        "x"         : [0.0],
        "y"         : [100.0],
        "z"         : [100.0],
    },
    { #4
        "line"      : {"color": LEG_COLR, "width": LEG_OUTLINE_WIDTH},
        "name"      : "leg 1",
        "showlegend": False,
        "type"      : "scatter3d",
        "uid"       : "f217db57-fe6e-4b40-90f8-4e1c20ef595e",
        "x"         : [100.0, 200.0, 300.0, 300.0],
        "y"         : [0.0, 0.0, 0.0, 0.0],
        "z"         : [100.0, 100.0, 100.0, 0.0],
    },
    { #5
        "line"      : {"color": LEG_COLR, "width": LEG_OUTLINE_WIDTH},
        "name"      : "leg 2",
        "showlegend": False,
        "type"      : "scatter3d",
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [100.0, 170.71067811865476, 241.4213562373095, 241.4213562373095],
        "y"         : [100.0, 170.71067811865476, 241.42135623730948, 241.42135623730948],
        "z"         : [100.0, 100.0, 100.0, 0.0],
    },
    { #6
        "line"      : {"color": LEG_COLR, "width": LEG_OUTLINE_WIDTH},
        "name"      : "leg 3",
        "showlegend": False,
        "type"      : "scatter3d",
        "uid"       : "9f13f416-f2b7-4eb7-993c-1e26e2e7a908",
        "x"         : [-100.0, -170.71067811865476, -241.42135623730948, -241.42135623730948],
        "y"         : [100.0, 170.71067811865476, 241.4213562373095, 241.4213562373095],
        "z"         : [100.0, 100.0, 100.0, 0.0],
    },
    { #7
        "line"      : {"color": LEG_COLR, "width": LEG_OUTLINE_WIDTH},
        "name"      : "leg 4",
        "showlegend": False,
        "type"      : "scatter3d",
        "uid"       : "0d426c49-19a4-4051-b938-81b30c962dff",
        "x"         : [-100.0, -200.0, -300.0, -300.0],
        "y"         : [0.0,1.2246467991473532e-14,2.4492935982947064e-14,2.4492935982947064e-14,],
        "z"         : [100.0, 100.0, 100.0, 0.0],
    },
    { #8
        "line"      : {"color": LEG_COLR, "width": LEG_OUTLINE_WIDTH},
        "name"      : "leg 5",
        "showlegend": False,
        "type"      : "scatter3d",
        "uid"       : "5ba25594-2fb5-407e-a16f-118f12769e28",
        "x"         : [-100.0, -170.71067811865476, -241.42135623730954, -241.42135623730954],
        "y"         : [-100.0, -170.71067811865476, -241.42135623730948, -241.42135623730948],
        "z"         : [100.0, 100.0, 100.0, 0.0],
    },
    { #9
        "line"      : {"color": LEG_COLR, "width": LEG_OUTLINE_WIDTH},
        "name"      : "leg 6",
        "showlegend": False,
        "type"      : "scatter3d",
        "uid"       : "fa4b5f98-7d68-4eb9-bd38-a6f8dabef8a4",
        "x"         : [100.0, 170.71067811865476, 241.42135623730948, 241.42135623730948],
        "y"         : [-100.0, -170.71067811865476, -241.42135623730954, -241.42135623730954],
        "z"         : [100.0, 100.0, 100.0, 0.0],
    },
    { #10
        "name"      : "support polygon mesh",
        "showlegend": True,
        "type"      : "mesh3d",
        "opacity"   : SUPRT_POLY_MESH_OPAC,
        "color"     : "#ffa8a8",
        "uid"       : "1f821e07-2c02-4a64-8ce3-61ecfe2a91b6",
        "x"         : [    300.0,    241.4213562373095,    -241.42135623730948,    -300.0,    -241.42135623730954,    241.42135623730948,],
        "y"         : [    0.0,    241.42135623730948,    241.4213562373095,    2.4492935982947064e-14,    -241.42135623730948,    -241.42135623730954,],
        "z"         : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    },
    { #11
        "line"      : {"color": "#2f3640", "width": 2},
        "name"      : "hexapod x",
        "mode"      : "lines",
        "showlegend": False,
        "opacity"   : 1.0,
        "type"      : "scatter3d",
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0.0, 50.0],
        "y"         : [0.0, 0.0],
        "z"         : [100.0, 100.0],
    },
    { #12
        "line"      : {"color": "#e67e22", "width": 2},
        "name"      : "hexapod y",
        "mode"      : "lines",
        "showlegend": False,
        "opacity"   : 1.0,
        "type"      : "scatter3d",
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0.0, 0.0],
        "y"         : [0.0, 50.0],
        "z"         : [100.0, 100.0],
    },
    { #13
        "line"      : {"color": "#0097e6", "width": 2},
        "name"      : "hexapod z",
        "mode"      : "lines",
        "showlegend": False,
        "opacity"   : 1.0,
        "type"      : "scatter3d",
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0.0, 0.0],
        "y"         : [0.0, 0.0],
        "z"         : [100.0, 150.0],
    },
    { #14
        "line"      : {"color": "#e62222", "width": 5},
        "name"      : "x direction",
        "showlegend": False,
        "mode"      : "lines",
        "opacity"   : 1.0,
        "type"      : "scatter3d",
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0, 50],
        "y"         : [0, 0],
        "z"         : [0, 0],
    },
    { #15
        "line"      : {"color": "#00ff00", "width": 5},
        "name"      : "y direction",
        "showlegend": False,
        "mode"      : "lines",
        "opacity"   : 1.0,
        "type"      : "scatter3d",
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0, 0],
        "y"         : [0, 50],
        "z"         : [0, 0],
    },
    { #16
        "line"      : {"color": "#0000ff", "width": 5},
        "name"      : "z direction",
        "showlegend": False,
        "mode"      : "lines",
        "opacity"   : 1.0,
        "type"      : "scatter3d",
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0, 0],
        "y"         : [0, 0],
        "z"         : [0, 50],
    },
]

HEXAPOD_FIGURE = {
    "data": FIG_DATA,
    "layout": {
        "paper_bgcolor": PAPER_BG_COLR,

        "hovermode"    : "closest",

        "legend"       : {"x": 0,"y": 0,"bgcolor": LEGENDS_BG_COLR,
                           "font": {"family": "courier", "size": 12, "color": LEGEND_FONT_COLR}
                         },

        "margin"       : {"b": 20, "l": 10, "r": 10, "t": 20
                         },

        "scene"        : {"aspectmode" : "manual",
                          
                          "aspectratio": {"x": 1, "y": 1, "z": 1},

                          "camera": {
                                    "center": {"x": 0.0348603742736399,"y": 0.16963779995083,"z": -0.394903376555686,},
                                    "eye"   : {"x": 0.193913968006015,"y": 0.45997575676993,"z": -0.111568465000231},
                                    "up"    : {"x": 0, "y": 0, "z": 1},
                                    },

                          "xaxis": {
                                   "nticks": 1,"range": [-600, 600],"zerolinecolor": AXIS_ZERO_LINE_COLR,
                                   "showbackground": True
                                   },

                          "yaxis": {"nticks": 1,"range": [-600, 600],"zerolinecolor": AXIS_ZERO_LINE_COLR,
                                    "showbackground": True 
                                   },

                          "zaxis": {"nticks": 1,"range": [-600, -10],"zerolinecolor": AXIS_ZERO_LINE_COLR,
                                    "showbackground": True,"backgroundcolor": GROUND_COLR
                                   },
                        }
    },
}

AXIS_TMPLT = [{ 
        "line"      : {"color": "#e62222", "width": 5}      ,
        "name"      : "x direction"                         ,
        "showlegend": False                                 ,
        "mode"      : "lines"                               ,
        "opacity"   : 1.0                                   ,
        "type"      : "scatter3d"                           ,
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0, 0],
        "y"         : [0, 0],
        "z"         : [0, 0],
    },
    { 
        "line"      : {"color": "#00ff00", "width": 5}      ,
        "name"      : "y direction"                         ,
        "showlegend": False                                 ,
        "mode"      : "lines"                               ,
        "opacity"   : 1.0                                   ,
        "type"      : "scatter3d"                           ,
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0, 0],
        "y"         : [0, 0],
        "z"         : [0, 0],
    },
    { 
        "line"      : {"color": "#0000ff", "width": 5}      ,
        "name"      : "z direction"                         ,
        "showlegend": False                                 ,
        "mode"      : "lines"                               ,
        "opacity"   : 1.0                                   ,
        "type"      : "scatter3d"                           ,
        "uid"       : "d5690122-cd54-460d-ab3e-1f910eb88f0f",
        "x"         : [0, 0],
        "y"         : [0, 0],
        "z"         : [0, 0],
    }]

class BotFigureType:
    __slots__ = ("figure_dic","name")

    def __init__(self,name:str="",figure_dic:dict=None):

        # Type check
        if figure_dic is not None: 
            if (isinstance(figure_dic,dict) == False or isinstance(name,str)== False):
                raise NameError('fatal error: Incorrect arguments type')
        
        if figure_dic == None:
            self.figure_dic = deepcopy(HEXAPOD_FIGURE)
        else: 
            self.figure_dic = deepcopy(figure_dic)

    def draw_hexapod(self,bdy_pts_wwrd :HexgnPtsType,ctraj_legs_wwrd:CarSqsType,
                          conta_pts_wrd:BotVecArr   ,vp_act:ValvPumpActType=None):
        """
        All points are with respect to world coordinate
        """
        cob    = bdy_pts_wwrd[6]
        head   = bdy_pts_wwrd[7]
        # Body Surface Mesh
        for i in range(7):
            [x,y,z] = bdy_pts_wwrd[i%6]
     
            self.figure_dic["data"][0]["x"][i] = x
            self.figure_dic["data"][0]["y"][i] = y
            self.figure_dic["data"][0]["z"][i] = z

        # Body Outline
        self.figure_dic["data"][1]["x"] = self.figure_dic["data"][0]["x"]
        self.figure_dic["data"][1]["y"] = self.figure_dic["data"][0]["y"]
        self.figure_dic["data"][1]["z"] = self.figure_dic["data"][0]["z"]

        self.figure_dic["data"][2]["x"] = [cob [0]]
        self.figure_dic["data"][2]["y"] = [cob [1]]
        self.figure_dic["data"][2]["z"] = [cob [2]]

        self.figure_dic["data"][3]["x"] = [head[0]]
        self.figure_dic["data"][3]["y"] = [head[1]]
        self.figure_dic["data"][3]["z"] = [head[2]]

        leg_id = 0

        if vp_act != None:
            for n,one_act in zip(range(4, 10),vp_act):
                [x_lst,y_lst,z_lst]=ctraj_legs_wwrd.get_traj_ileg(leg_id)
                self.figure_dic["data"][n]["x"] = x_lst
                self.figure_dic["data"][n]["y"] = y_lst
                self.figure_dic["data"][n]["z"] = z_lst
                leg_id+=1

                if(one_act == vp_act.TURN_OFF): # Assign on-vpump color 
                    self.figure_dic["data"][n]["line"]["color"] = LEG_COLR_VP_OFF
                else:
                    self.figure_dic["data"][n]["line"]["color"] = LEG_COLR
        else: 
            for n in range(4, 10):
                [x_lst,y_lst,z_lst] = ctraj_legs_wwrd.get_traj_ileg(leg_id)
                self.figure_dic["data"][n]["x"] = x_lst
                self.figure_dic["data"][n]["y"] = y_lst
                self.figure_dic["data"][n]["z"] = z_lst
                leg_id+=1

            
        # Hexapod Support Polygon Draw a mesh for body contact on ground
        dz = -1  # Mesh must be slightly below ground

        self.figure_dic["data"][10]["x"] = conta_pts_wrd.get_by_axis('x')
        self.figure_dic["data"][10]["y"] = conta_pts_wrd.get_by_axis('y')
        self.figure_dic["data"][10]["z"] = list(np.array(conta_pts_wrd.get_by_axis('z'))+dz)

    def draw_scene(self,cob_wwrd:AxisType,axis_scale:float,\
                   scene_range_xyz:list=[0,0,0]):
        """
        scene_range_xyz: [x,y,z]
        """
        self.figure_dic["layout"]["scene"]["xaxis"]["range"] = scene_range_xyz[0]
        self.figure_dic["layout"]["scene"]["yaxis"]["range"] = scene_range_xyz[1]
        self.figure_dic["layout"]["scene"]["zaxis"]["range"] = scene_range_xyz[2]

        self.figure_dic["data"][11]["x"] = [cob_wwrd[3][0], cob_wwrd[0][0]]
        self.figure_dic["data"][11]["y"] = [cob_wwrd[3][1], cob_wwrd[0][1]]
        self.figure_dic["data"][11]["z"] = [cob_wwrd[3][2], cob_wwrd[0][2]]

        self.figure_dic["data"][12]["x"] = [cob_wwrd[3][0], cob_wwrd[1][0]]
        self.figure_dic["data"][12]["y"] = [cob_wwrd[3][1], cob_wwrd[1][1]]
        self.figure_dic["data"][12]["z"] = [cob_wwrd[3][2], cob_wwrd[1][2]]

        self.figure_dic["data"][13]["x"] = [cob_wwrd[3][0], cob_wwrd[2][0]]
        self.figure_dic["data"][13]["y"] = [cob_wwrd[3][1], cob_wwrd[2][1]]
        self.figure_dic["data"][13]["z"] = [cob_wwrd[3][2], cob_wwrd[2][2]]

        # Scale the global coordinate frame
        self.figure_dic["data"][14]["x"] = [0, axis_scale]
        self.figure_dic["data"][14]["y"] = [0,          0]
        self.figure_dic["data"][14]["z"] = [0,          0]

        self.figure_dic["data"][15]["x"] = [0,          0]
        self.figure_dic["data"][15]["y"] = [0, axis_scale]
        self.figure_dic["data"][15]["z"] = [0,          0]

        self.figure_dic["data"][16]["x"] = [0,          0]
        self.figure_dic["data"][16]["y"] = [0,          0]
        self.figure_dic["data"][16]["z"] = [0, axis_scale]    

    def draw_odom(self,traces:List[AxisType]):
        new_axis_line = self.set_new_axis_line(traces)
        self.figure_dic["data"] = self.figure_dic["data"] +new_axis_line

    def change_camera_view(self,camera):
        self.figure_dic["layout"]["scene"]["camera"] = camera

    def set_new_axis_line(self,traces:List[AxisType]):
        """
        Given a list of axis trances, generate axis line, and append to current dictionary(self.figure_dic)
        """
        draw_msg = []
        for trace in traces:

            msg_tplt = deepcopy(AXIS_TMPLT)
            # Scale the global coordinate frame
            msg_tplt[0]["x"][0] = trace[3][0]
            msg_tplt[0]["y"][0] = trace[3][1]
            msg_tplt[0]["z"][0] = trace[3][2]
            msg_tplt[0]["x"][1] = trace[0][0]
            msg_tplt[0]["y"][1] = trace[0][1]
            msg_tplt[0]["z"][1] = trace[0][2]

            msg_tplt[1]["x"][0] = trace[3][0]
            msg_tplt[1]["y"][0] = trace[3][1]
            msg_tplt[1]["z"][0] = trace[3][2]
            msg_tplt[1]["x"][1] = trace[1][0]
            msg_tplt[1]["y"][1] = trace[1][1]
            msg_tplt[1]["z"][1] = trace[1][2]

            msg_tplt[2]["x"][0] = trace[3][0]
            msg_tplt[2]["y"][0] = trace[3][1]
            msg_tplt[2]["z"][0] = trace[3][2]
            msg_tplt[2]["x"][1] = trace[2][0]
            msg_tplt[2]["y"][1] = trace[2][1]
            msg_tplt[2]["z"][1] = trace[2][2]

            draw_msg = draw_msg+msg_tplt
        return draw_msg

    def set_fig_dic(self,figure_dic:dict):
        self.figure_dic = figure_dic
    
    def set_cam_view(self,cam_view):
        """
        Set camera view
        came_view type: 
            "camera": {
              "center": {"x": 0.03,"y": 0.1,"z": -0.39,},
              "eye"   : {"x": 0.1 ,"y": 0.4,"z": -0.1  },
              "up"    : {"x": 0   ,"y": 0  ,"z": 1     },
              }
        """
        self.figure_dic["layout"]["scene"]["camera"] = cam_view

    def set_fig_by_json(self,figure_json:str):
        fig_dic = json.loads(figure_json)
        self.set_fig_dic(fig_dic)   


    def get_fig_dic(self)->dict:
        return self.figure_dic
    
    def get_fig_json_str(self)->str:
        fig_dic = self.get_fig_dic()
        json_str = json.dumps(fig_dic)
        return json_str
    
