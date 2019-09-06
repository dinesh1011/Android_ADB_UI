import os
import sys

class mainClass():
    __alldetails = dict(os.environ)
    def __init__(self):
        for key, val in self.__alldetails.items():
            print(key + " :: " + val)

    def getPlatform(self):
        print("OS", ' :: ', sys.platform)

'''if __name__ == "__main__":
    myclass =  mainClass()
    print(myclass._mainClass__alldetails)'''

def newFunction(inputFunction):
    print("executing inputFunction")
    def newOutFunction(**args):
        inputFunction(**args)
        print(args)
    outFunction = newOutFunction
    print("return outputFunction")
    return(outFunction)

@newFunction
def myFunction(a,b):
    print(a**b)

myFunction(a=2,b=4)