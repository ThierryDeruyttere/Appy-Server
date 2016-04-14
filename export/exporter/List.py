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
        super().__init__(name, info)
        self.parseListProps(info["properties"])
        self.html = compiler.compile(readFile("export/templates/HTML/list.html"))

    def parseListProps(self, props):
        self.genItems = []

        for comp in props["newItemComponents"]:
            name = comp["name"]
            compType = comp["type"]

            self.genItems.append(componentsClass[compType](name, comp, inList=True))

    def generate(self):
        comp = {}
        comp["type"] = "List"
        comp["binding"] = {}
        comp["properties"] = self.props

        # Bindings
        self.createBinding(comp["binding"], "visibility")
        self.createBinding(comp["binding"], "dim")
        self.createBinding(comp["binding"], "page")
        self.createBinding(comp["binding"], "genitems")

        comp["binding"]["itemcomponent"] = self.name.lower() + "_component"
        comp["genItems"] = {}
        comp["genItems"]["itemcomponent"] = self.name.lower() + "_component"
        comp["genItems"]["html"] = ""

        for genitem in self.genItems:
            _, compData = genitem.generate()
            comp["genItems"]["html"] += compData["html"]

        # Properties
        comp["html"] = self.html(comp["binding"])
        return self.name, comp, True
