from pybars import Compiler
from export.utils import readFile
from .Dimension import Dimension
compiler = Compiler()

class Component:
    def __init__(self, name, info, inList=False, listDim=None):
        self.name = name
        self.props = info["properties"]
        self.parseCompProps(info["properties"])
        self.inList = inList
        self.listDim = listDim
        self.setCompDimensions()

    def parseCompProps(self, props):
        self.visibile = props["visibility"]
        self.page = props["page"]
        self.dim = Dimension(props["dim"])

    def setCompDimensions(self):
        if not self.inList:
            width = Dimension.appWidth
            height = Dimension.appHeight
            self.props["position"] = "absolute"
        else:
            width = self.listDim.width
            height = self.listDim.height
            self.props["position"] = "relative"

        self.props["width"] = str(self.dim.width / width * 100) + "%"
        self.props["height"] = str(self.dim.height / height * 100) + "%"
        self.props["row"] = str(self.dim.row / height * 100) + "%"
        self.props["column"] = str(self.dim.column / width * 100) + "%"

    def createBinding(self, bindings, bindingName):
        if not self.inList:
            bindings[bindingName] = "components." + self.name + "." + bindingName
        else:
            specials = ["width", "height", "row", "column", "position"]
            if bindingName in specials:
                bindings[bindingName] = "'" + self.props[bindingName] + "'"
            else:
                bindings[bindingName] = "compdata." + self.name + "." + bindingName

    def generate(self, triggers):
        abstract
