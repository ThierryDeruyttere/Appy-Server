from pybars import Compiler
from export.utils import readFile
from .Dimension import Dimension
compiler = Compiler()

def readFile(filePath):
    f = open(filePath, 'r')
    return f.read()

class Component:
    def __init__(self, name, info, inList=False):
        self.name = name
        self.props = info["properties"]
        self.parseCompProps(info["properties"])
        self.inList = inList

    def parseCompProps(self, props):
        self.visibile = props["visibility"]
        self.page = props["page"]
        self.dim = Dimension(props["dim"])

    def createBinding(self, bindings, bindingName):
        if not self.inList:
            bindings[bindingName] = "components." + self.name + "." + bindingName
        else:
            bindings[bindingName] = "compdata." + self.name + "." + bindingName

    def generate(self):
        abstract
