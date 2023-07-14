# reference: https://stackoverflow.com/questions/40252765/overriding-other-rmul-with-your-classs-mul

from spatialmath import SE3 

class B:
    def __init__(self,a):
      self.a = a
            

    def __mul__(self, scalar):
      print("Bmul")
      r = self.a+1
      return r
    def __rmul__(self, scalar):
      print("Brmul")
      r = self.a+2
      return r
    
    __array_priority__ = 10000

    
class A:
    def __init__(self):

      self.T = {0:{"T":SE3.Trans(1,2,3)}}
            

    def __mul__(left,right):
      print("Amul")
      r = left.T[0]["T"]*right
      return r
    
    def __rmul__(right,left ):

      # elif isinstance(right, (list, tuple, np.ndarray)):
      print("Armul")

      r = right.T[0]["T"]*left

      return r 


def test1():
   
  ts  = A()
  t1 = SE3.Trans(4,5,6)

  #rst = ts*t1
  #print(rst)

  rst = t1*ts
  
  #rst = ts*[1,2,3]
  #print("2-----")
  #rst = ts*t1

  print(rst)

if __name__ == "__main__":
   

  test1()
