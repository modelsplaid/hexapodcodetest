
import json 
import copy
import time

class CarTraj:


    __slots__ = ("ctraj","name")
    def __init__(self, ctraj = None, name=None):
        ctraj_tmplt = \
            {
            0: {"x": [195 ,195 ,195 , 195],"y": [ -30, -30,  30,  30],"z": [10,0,0,10],"name": "right-middle","id": 0},
            1: {"x": [161 ,161 ,161 , 161],"y": [  89,  89, 149, 149],"z": [10,0,0,10],"name": "right-front" ,"id": 1},
            2: {"x": [-161,-161,-161,-161],"y": [ 149, 149,  89,  89],"z": [10,0,0,10],"name": "left-front"  ,"id": 2},
            3: {"x": [-195,-195,-195,-195],"y": [  30,  30, -30, -30],"z": [10,0,0,10],"name": "left-middle" ,"id": 3},
            4: {"x": [-161,-161,-161,-161],"y": [ -88,-88 ,-148,-148],"z": [10,0,0,10],"name": "left-back"   ,"id": 4},
            5: {"x": [161 ,161 ,161 , 161],"y": [-149,-149, -89, -89],"z": [10,0,0,10],"name": "right-back"  ,"id": 5}
            }
        
        if (ctraj == None):
            self.ctraj = ctraj_tmplt
        else: 
            self.ctraj = ctraj
             
        self.name  = name
    def get_ctraj_dic(self):
        return self.ctraj

    def __str__(self):

        # Format row 
        len_arr = len(self.ctraj[0]["x"])
        sr = ""


        for i in range(len_arr):
            x = self.ctraj[0]["x"][i]
            y = self.ctraj[0]["y"][i]
            z = self.ctraj[0]["z"][i]
            sr = sr+f"[{x:>+4.2f},{y:>+4.2f},{z:>+4.2f}], "



        #s = f"ctraj_tmplt(x={a}, name='{self.name}')"
        return sr
     
class PulseWalk:
    __slots__ = (
          "params_gaits" ,"params_gaits" ,"jtrajs","vpump_sqs","gait_cmpensat","trght_gaits"
          )
    
    def __init__(self,params_gaits,hexapod,trght_gaits):
        pass
      
    def pwalk_rtwd_ctraj(self):
        '''
        Generate rightward walk cartesian trajectories w.r.t. gnd coordinate
        '''
        ctraj = {\
            0: {"x": [], "y": [], "z": [], "name": "right-middle", "id": 0},
            1: {"x": [], "y": [], "z": [], "name": "right-front" , "id": 1},
            2: {"x": [], "y": [], "z": [], "name": "left-front"  , "id": 2},
            3: {"x": [], "y": [], "z": [], "name": "left-middle" , "id": 3},
            4: {"x": [], "y": [], "z": [], "name": "left-back"   , "id": 4},
            5: {"x": [], "y": [], "z": [], "name": "right-back"  , "id": 5}}


        pass
def load_json():
    out_file = open("turn_right_gaits.json", "r") 
    trght_gaits = json.load(out_file)


if __name__ == "__main__":

        load_json()
        ct1 = CarTraj()
        print(ct1)