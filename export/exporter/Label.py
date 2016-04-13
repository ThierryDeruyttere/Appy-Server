from .Component import *

class Label(Component):

    def __init__(self, name, info):
        super.__init__(name, info)
        self.parseLabelComponent(info["properties"])

        self.hmtl = compiler.compile(readFile("export/templates/HTML/label.html"))

    def parseLabelComponent(self, props):
        self.text = props["text"]

    def generate(self):
        return self.html({
            "dim": self.dim.getDict(),
            "text": self.text,
            "visibility": self.visibile,
        })