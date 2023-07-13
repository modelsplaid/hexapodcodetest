class My_Class:
    K=3
    def __init__(self,a):
            print("init"+str(a))
            print(self.K)
            
    def __new__(cls,b):
            print("new" +str(b))
            print(cls.K)
            return super(My_Class, cls).__new__(cls)

a = My_Class(123)

