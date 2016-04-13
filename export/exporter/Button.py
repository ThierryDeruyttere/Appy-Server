from .Component import *

class Button(Component):

    def __init__(self, name, info):
        super.__init__(name, info)
        self.parseButtonProps(info["properties"])

        self.hmtl = compiler.compile(readFile("export/templates/HTML/button.html"))

    def parseButtonProps(self, props):
        self.text = props["text"]

    def generate(self):
        return self.html({
            "dim": self.dim.getDict(),
            "text": self.text,
            "click": None,
        })