def multiply(*argss):
    print(argss)
    z = 1
    for num in argss:
        z *= num
    print(z)

multiply(10, 9)

def print_kwargs(**kwargs):
        print(kwargs)

print_kwargs(kwargs_1="Shark", kwargs_2=4.5, kwargs_3=True)

def print_kwargs2(q,u=3,**kwargs):
        print(kwargs)
        print(q)
        print(u)

print_kwargs2(12,2,kwargs_1="Shark", kwargs_2=4.5, kwargs_3=True)
print_kwargs2(12,2)

class Robot():


    def __init__(
        self,
        links,
        name="noname",
        manufacturer="",
    ):
        print("links: "+str(links))
        print("name: "+str(name))
        print("manufacturer: "+str(manufacturer))


class DHRobot(Robot):
    def __init__(self, links, meshdir=None, **kwargs):
        #super().__init__(links,"the name", **kwargs)
        super().__init__(links, **kwargs)



#robot = DHRobot("the link", theargs="the args",anotherargs="another args")
robot = DHRobot(links="the link", name="hexa pod",manufacturer="modi")

isins = isinstance(robot,DHRobot)
print("is instance robot,DHRobot: "+str(isins) )

