class AB:
    c = 3

    @staticmethod
    def pta():
        print("ab")
        AB.c = 4
        print(AB.c)

AB.pta()
