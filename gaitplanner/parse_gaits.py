
import json 
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
    
    def set_one_pt(self,leg_idx,traj_idx,*args,**kwds):
        # Arguments: 
        # case 1: *args is pt=[0,0,0]
        # case 2: **kwds choises are:  x=number, y=number,z=number
        #
        # Example1 set a point: 
        #       ct1 = CarTraj(name="ct1")
        #       ct1.set_one_pt(0,0,[1,2,3])
        #       print("arr"+str(ct1.get_one_pt(0,0)))
        #
        # Example2 set a point by specifying one or more axis: 
        #       ct1.set_one_pt(1,0,x=9,y=8,z=7)
        #       print("separate"+str(ct1.get_one_pt(1,0)))
        #       
        #       ct1.set_one_pt(3,2,x=99,y=88)
        #       print("separate"+str(ct1.get_one_pt(3,2)))

        if len(args) == 1 and isinstance(args[0], list):

            self.ctraj[leg_idx]["x"][traj_idx] = args[0][0]
            self.ctraj[leg_idx]["y"][traj_idx] = args[0][1]
            self.ctraj[leg_idx]["z"][traj_idx] = args[0][2]
            return 
        
        if len(args) == 0 and len(kwds.keys()) > 0:
            for axis_name in kwds.keys(): # keys are any from : 'x' , 'y' , 'z' 
                self.ctraj[leg_idx][axis_name][traj_idx] = kwds[axis_name]
            return
        
        print("args: "+str(args))
        print("kwds: "+str(kwds))
        raise NameError('fatal error: Incorrect arguments')
    
    def get_one_pt(self,leg_idx,traj_idx):
        x = self.ctraj[leg_idx]["x"][traj_idx]
        y = self.ctraj[leg_idx]["y"][traj_idx]
        z = self.ctraj[leg_idx]["z"][traj_idx]

        return [x,y,z]
    
    def __add__(self,d):
        # Reload the add("+") sign, as append operation
        len_legs = len(self.ctraj)
        for j in range(len_legs):
            self.ctraj[j]["x"] = self.ctraj[j]["x"] + d.ctraj[j]["x"]
            self.ctraj[j]["y"] = self.ctraj[j]["y"] + d.ctraj[j]["y"]
            self.ctraj[j]["z"] = self.ctraj[j]["z"] + d.ctraj[j]["z"]

        return(CarTraj(self.ctraj,"append("+self.name+"," +d.name+")" ))

    def __str__(self):

        # Format row coord value
        len_arr  = len(self.ctraj[0]["x"])
        len_legs = len(self.ctraj)
        sr_val_ar = [""]*len_legs

        for j in range(len_legs):
            x_str = "x: ["
            y_str = " y: ["
            z_str = " z: ["
            for i in range(len_arr):
                x = self.ctraj[j]["x"][i]
                y = self.ctraj[j]["y"][i]
                z = self.ctraj[j]["z"][i]

                x_str = x_str + f"{x:+8.2f},"
                y_str = y_str + f"{y:+8.2f},"
                z_str = z_str + f"{z:+8.2f},"

            sr_val_ar[j] = x_str+"],"+y_str+"],"+z_str[0:-1]+"]"

        # Format names
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = self.ctraj[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + "coords: "+ sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]

        return full_str
     
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


def test_CarTraj():

    load_json()


    # Test set and get pt 
    ctraj_tmplt = \
        {
        0: {"x": [195 ,195 ,195 , 195],"y": [ -30, -30,  30,  30],"z": [10,0,0,10],"name": "right-middle","id": 0},
        1: {"x": [161 ,161 ,161 , 161],"y": [  89,  89, 149, 149],"z": [10,0,0,10],"name": "right-front" ,"id": 1},
        2: {"x": [-161,-161,-161,-161],"y": [ 149, 149,  89,  89],"z": [10,0,0,10],"name": "left-front"  ,"id": 2},
        3: {"x": [-195,-195,-195,-195],"y": [  30,  30, -30, -30],"z": [10,0,0,10],"name": "left-middle" ,"id": 3},
        4: {"x": [-161,-161,-161,-161],"y": [ -88,-88 ,-148,-148],"z": [10,0,0,10],"name": "left-back"   ,"id": 4},
        5: {"x": [161 ,161 ,161 , 161],"y": [-149,-149, -89, -89],"z": [10,0,0,10],"name": "right-back"  ,"id": 5}
        }
    ct1 = CarTraj(ctraj_tmplt,name="ct1")
    # Test Appending 
    #ct2 = CarTraj(ctraj,name="ct2")
    #print(str(ct1+ct2)+"name: "+(ct1+ct2).name )

    ct1.set_one_pt(0,0,[1,2,3])
    print("arr"+str(ct1.get_one_pt(0,0)))

    ct1.set_one_pt(1,0,x=9,y=8,z=7)
    print("separate"+str(ct1.get_one_pt(1,0)))

    ct1.set_one_pt(3,2,x=99,y=88)
    print("separate"+str(ct1.get_one_pt(3,2)))
if __name__ == "__main__":
    test_CarTraj()
