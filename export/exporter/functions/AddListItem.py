from .Function import *

class AddListItem(Function):
    def __init__(self, name, info):
        Function.__init__(self, name, info)
        self.js = compiler.compile(readFile("export/templates/js/addListItem.js"))

    def generate(self):
        data = {
        }

        return {
            "name": "method_" + self.name,
            "js": self.js(data)
        }, self.triggers, []
