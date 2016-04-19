from .Component import *

class Image(Component):

    def __init__(self, name, info, inList=False, listDim=None):
        super().__init__(name, info, inList, listDim)
        self.parseImageProps(info["properties"])

        self.html = compiler.compile(readFile("export/templates/HTML/image.html"))

    def parseImageProps(self, props):
        self.file = props["file"]

    def generate(self):
        comp = {}
        comp["type"] = "Textbox"
        comp["binding"] = {}
        comp["properties"] = self.props

        # Bindings
        self.createBinding(comp["binding"], "visibility")
        self.createBinding(comp["binding"], "dim")
        self.createBinding(comp["binding"], "text")
        self.createBinding(comp["binding"], "file")
        self.createBinding(comp["binding"], "position")

        # Properties
        comp["html"] = self.html(comp["binding"])

        return self.name, comp
