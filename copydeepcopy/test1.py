from copy import copy, deepcopy
class A:
    __slots__ = ("name","tran_bdy_cords","f", "m", "s","v","z")
    def __init__(self):
        print ('init')
        self.v = 10
        self.z = {"a":2,"b":3,"c":4}

    def __copy__(self):
        cls = self.__class__

        print(cls)
        result = cls.__new__(cls)
        print(result)
        result.__dict__.update(self.__dict__)
        print(result)
        print(self.__dict__)
        return result

    def trans(self):
        cls = self.__class__ 
        result = cls.__new__(cls)
        result.z["a"] = 99 

        return result
        
    def aa(self): 
        print(type(self.__dict__.items()))

    def __deepcopy__(self, memo):

        cls = self.__class__
        result = cls.__new__(cls)

        print("cls: "+str(cls) )
        print("result: "+str(result) )
        print(type(self.__dict__))
        for k, v in self.__dict__.items():
            setattr(cls, k, deepcopy(v, memo))
        return result



def test_deepcopy():
    print("A: "+str( A))
    print("a: "+str( a))

    print("-------test1")
    a.z["a"] = 11
    b1  = copy(a)
    b1.z["a"] = 12

    print(a.z["a"])
    print(b1.z["a"])

    print("-------test2")
    a1 = A()
    a1.z["a"] = 7
    b2  = deepcopy(a1)
    b2.z["a"] = 19

    print(a1.z["a"])
    print(b2.z["a"])

    print("------test3")

    b3 = a1.trans()

    print(a1.z["a"])
    print(b3.z["a"])


    b2  = deepcopy(a1)
    b2.aa()

def testslots():
    a = A()
    print(a.__slots__)

testslots()