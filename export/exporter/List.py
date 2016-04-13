from .Component import *

class List(Component):

    def __init__(self, name, info):
        super.__init__(name, info)
        self.html = compiler.compile(readFile("export/templates/HTML/textbox.html"))

    def generate(self):
        pass
