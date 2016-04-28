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
        self.newItemComponents = []
        for comp in props["newItemComponents"]:
            name = comp["name"]
            compType = comp["type"]
            self.newItemComponents.append(componentsClass[compType](name, comp, True, self.dim))

    def generate(self, triggers):
        comp = {}
        comp["type"] = "List"
        comp["binding"] = {}
        comp["properties"] = self.props

        # Bindings
        self.createBinding(comp["binding"], "visibility")
        self.createBinding(comp["binding"], "page")
        self.createBinding(comp["binding"], "genitems")
        self.createBinding(comp["binding"], "width")
        self.createBinding(comp["binding"], "height")
        self.createBinding(comp["binding"], "row")
        self.createBinding(comp["binding"], "column")
        self.createBinding(comp["binding"], "position")

        comp["binding"]["itemcomponent"] = self.name.lower() + "_component"
        comp["genItems"] = {}
        comp["genItems"]["itemcomponent"] = self.name.lower() + "_component"
        comp["genItems"]["html"] = "<div class=\"listItem\">"

        #Add vm to triggers

        for key, val in triggers.items():
            d = []
            for t in val:
                d.append('vm.' + t)

            triggers[key] = d

        for genitem in self.newItemComponents:
            _, compData, _ = genitem.generate(triggers)
            comp["genItems"]["html"] += compData["html"]
        comp["genItems"]["html"] += "</div>"

        # Properties
        comp["html"] = self.html(comp["binding"])
        return self.name, comp, True
