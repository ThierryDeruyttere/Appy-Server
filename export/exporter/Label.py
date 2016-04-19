from .Component import *

class Label(Component):

    def __init__(self, name, info, inList=False, listDim=None):
        super().__init__(name, info, inList, listDim)
        self.parseLabelComponent(info["properties"])

        self.html = compiler.compile(readFile("export/templates/HTML/label.html"))

    def parseLabelComponent(self, props):
        self.text = props["text"]

    def generate(self):
        comp = {}
        comp["type"] = "Label"
        comp["binding"] = {}
        comp["properties"] = self.props

        # Bindings
        self.createBinding(comp["binding"], "visibility")
        self.createBinding(comp["binding"], "text")
        self.createBinding(comp["binding"], "page")
        self.createBinding(comp["binding"], "width")
        self.createBinding(comp["binding"], "height")
        self.createBinding(comp["binding"], "row")
        self.createBinding(comp["binding"], "column")

        # Properties
        comp["html"] = self.html(comp["binding"])

        return self.name, comp
