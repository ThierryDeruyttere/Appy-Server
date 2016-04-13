from .Component import *

class Button(Component):

    def __init__(self, name, info):
        super().__init__(name, info)
        self.parseButtonProps(info["properties"])

        self.html = compiler.compile(readFile("export/templates/HTML/button.html"))

    def parseButtonProps(self, props):
        self.text = props["text"]

    def generate(self):
        comp = {}
        comp["type"] = "Button"
        comp["binding"] = {}
        comp["properties"] = self.props

        # Bindings
        self.createBinding(comp["binding"], "visibility")
        self.createBinding(comp["binding"], "dim")
        self.createBinding(comp["binding"], "text")
        self.createBinding(comp["binding"], "page")

        # Properties
        comp["html"] = self.html(comp["binding"])

        return self.name, comp
