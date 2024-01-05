import sys
sys.path.append("../")
import numpy as np
from    warnings        import warn
from    typing          import List, Union
from    spatialmath     import SE3
from    copy            import deepcopy
from    custom_type.bot_cart_type\
                        import BotCartType


class AxisType():
    __slots__ = ("axis_pts","name")

    def __init__(self,name="",initval=None):
        self.name = name
        if initval == None:
            self.axis_pts = {
                        0:{"pt":[1,0,0],"name":"x"},
                        1:{"pt":[0,1,0],"name":"y"},
                        2:{"pt":[0,0,1],"name":"z"},
                        3:{"pt":[0,0,0],"name":"o"}
                       }
        else: 
            self.axis_pts = {
                        0:{"pt":[initval,0,0],"name":"x"},
                        1:{"pt":[0,initval,0],"name":"y"},
                        2:{"pt":[0,0,initval],"name":"z"},
                        3:{"pt":[0,0,0      ],"name":"o"}
                       }
        
    def norm_axis(self,idx:int=0)->List[Union[float,float,float]]:
        """
        Normalized axis coordinate
        param idx: 0--3, for x,y,z,origin axis
        Return: normalized axis
        """
        axis_pt = np.array(self.axis_pts[idx]["pt"])
        l2norm  = np.linalg.norm(axis_pt)

        return deepcopy((axis_pt/l2norm).tolist())
        
    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls         = self.__class__
        result      = cls.__new__(cls)

        result.axis_pts\
                    = deepcopy(self.axis_pts)
        result.name = deepcopy(self.name)

        return result
    
    def mat_dot_self(self,tran_cob:SE3):
        """
        Update by given transformation matrix from 

        Param : tran_cob: Given tans matrix
        return: Transformed  object
        """

        result = self.clone()
        # Translate matrices
        for key in range(len(self.axis_pts)):
            rs = tran_cob*self[key]
            result[key][0] = rs[0][0]
            result[key][1] = rs[1][0]
            result[key][2] = rs[2][0]

        # copy value 
        result.name = "trans from " +self.name
        return result

    def __rmul__(self,tran_cob:SE3):
        """
        Update by given transformation matrix from 

        Param : tran_cob: Given tans matrix
        return: Transformed  object
        Param : tran_cob: Given tans matrix
        return: Transformed AxisType object
        """

        if isinstance(tran_cob,SE3): 
            result = self.mat_dot_self(tran_cob)
            return result
        else:
            return NotImplemented 

    def __str__(self):
        gstr= self.name+":\n"

        for key in self.axis_pts:
            x = self.axis_pts[key]["pt"][0]
            y = self.axis_pts[key]["pt"][1]
            z = self.axis_pts[key]["pt"][2]

            xyz = f"{x:+4.3f}" + ","+ f"{y:+4.3f}" + ","+ f"{z:+4.3f}"
            gstr =gstr+self.axis_pts[key]["name"] +"-axis: "+xyz+"\n" 

        return gstr 

    def __getitem__(self, key:int=0)->List[Union[float,float,float]]:
        """
        Given index, return list of [x,y,z]

        """
        if isinstance(key,int) and key >=0 and key < len(self.axis_pts):

            pt = self.axis_pts[key]["pt"]
            return pt
        else: 
            warn("Failed to get value")
            print(type(key))

            return ([0,0,0])    
        
    def __setitem__(self,key:int=0,pt:List[Union[float,float,float]]=[0,0,0]):
        """
        Given key index and [x,y,z], set point
        """
        if isinstance(key,int) and key >=0 and key < len(self.axis_pts):
            self.axis_pts[key]["pt"] = pt 
            return True
        else: 
            warn("Failed to set value")
            return False          
def test_getset():
    at = AxisType("at")
    print(at)
    bt=SE3.Rx(3.1415926)*at
    print(bt)

if __name__ == "__main__":
    test_getset()