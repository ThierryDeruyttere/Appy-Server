from .Function import *

class Plus(Function):
    def __init__(self, name, info):
        Function.__init__(self,name,info)
        self.js = compiler.compile(readFile("export/templates/js/plus.js"))

    def generate(self):
        data = {
            "name": self.name,
            "left": self.params["left"],
            "right": self.params["right"]
        }

        return {
            "name": "computed_" + self.name,
            "js": self.js(data)
        }
