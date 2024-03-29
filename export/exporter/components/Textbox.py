from .Component import *

class Textbox(Component):

    def __init__(self, name, info, inList=False, listDim=None):
        super().__init__(name, info, inList, listDim)
        self.parseTextboxProps(info["properties"])
        self.html = compiler.compile(readFile("export/templates/HTML/textbox.html"))

    def parseTextboxProps(self, props):
        self.text = props["text"]

    def generate(self, triggers):
        comp = {}
        comp["type"] = "Textbox"
        comp["binding"] = {}
        comp["properties"] = self.props

        # Bindings
        self.createBinding(comp["binding"], "visibility")
        self.createBinding(comp["binding"], "dim")
        self.createBinding(comp["binding"], "text")
        self.createBinding(comp["binding"], "page")
        self.createBinding(comp["binding"], "width")
        self.createBinding(comp["binding"], "height")
        self.createBinding(comp["binding"], "row")
        self.createBinding(comp["binding"], "column")
        self.createBinding(comp["binding"], "position")

        # Properties
        comp["html"] = self.html(comp["binding"])

        return self.name, comp, self.inList
