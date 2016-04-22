from .Function import *

class Plus(Function):
    def __init__(self, name, info):
        Function.__init__(self,name,info)
        self.js = compiler.compile(readFile("export/templates/js/plus.js"))

    def generate(self):
        data = {
            "name": self.name,
            "left": "components." + self.params["left"],
            "right": "components." + self.params["right"]
        }

        return {
            "name": "method_" + self.name,
            "js": self.js(data)
        }, self.triggers, {"result": None}

