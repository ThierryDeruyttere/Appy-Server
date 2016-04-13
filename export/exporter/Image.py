from .Component import *

class Image(Component):

    def __init__(self, name, info):
        super.__init__(name, info)
        self.parseImageProps(info["properties"])

        self.hmtl = compiler.compile(readFile("export/templates/HTML/image.html"))

    def parseImageProps(self, props):
        self.file = props["file"]

    def generate(self):
        pass