from .Component import *
from .Button import Button
from .Image import Image
from .Textbox import Textbox
from .Label import Label

componentsClass = {
    "Button": Button,
    "Textbox": Textbox,
    "Image": Image,
    "Label": Label
}

class List(Component):

    def __init__(self, name, info):
        super.__init__(name, info)
        self.parseListProps(info["properties"])
        self.html = compiler.compile(readFile("export/templates/HTML/textbox.html"))

    def parseListProps(self, props):
        self.genItems = []
        self.newItemComponents = {}

        for comp in props["newItemComponents"]:
            name = self.name + "." + comp["name"]
            compType = comp["type"]
            self.newItemComponents[name](componentsClass[compType](name, comp))


    def generate(self):
        comp = {}
        comp["type"] = "List"
        comp["binding"] = {}
        comp["properties"] = self.props

        # Bindings
        self.createBinding(comp["binding"], "visibility")
        self.createBinding(comp["binding"], "dim")
        self.createBinding(comp["binding"], "page")

        # Properties
        listHtml = self.html(comp["binding"]) + "\n"
        genItems = {}
        for comp in self.newItemComponents:
            name, compData = comp.generate()
            genItems[name] = compData
            listHtml += compData["html"] + "\n"



        comp["html"] = listHtml


        #self.html(comp["binding"])

        return self.name, comp
