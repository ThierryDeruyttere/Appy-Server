from pybars import Compiler
from export.utils import readFile
from .Dimension import Dimension
compiler = Compiler()

def readFile(filePath):
    f = open(filePath, 'r')
    return f.read()

class Component:
    def __init__(self, name, info):
        self.name = name
        self.parseCompProps(info["properties"])

    def parseCompProps(self, props):
        self.visibile = props["visibility"]
        self.page = props["page"]
        self.dim = Dimension(props["dim"])


    def generate(self):
        abstract

