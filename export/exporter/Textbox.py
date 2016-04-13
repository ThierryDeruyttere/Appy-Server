from .Component import *

class Textbox(Component):

    def __init__(self, name, info):
        super.__init__(name, info)
        self.parseTextboxProps(info["properties"])
        self.hmtl = compiler.compile(readFile("export/templates/HTML/textbox.html"))

    def parseTextboxProps(self, props):
        self.text = props["text"]

    def generate(self):
        return self.html({
            "dim": self.dim.getDict(),
            "text": self.text,
            "visibility": self.visibile,
        })