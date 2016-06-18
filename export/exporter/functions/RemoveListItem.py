from .Function import *

class RemoveListItem(Function):
    def __init__(self, name, info, list):
        Function.__init__(self, name, info)
        self.js = compiler.compile(readFile("export/templates/js/removeListItem.js"))
        self.list = list

    def generate(self):
        data = { 'list': self.list.name,
        }

        return {
            "name": "method_" + self.name,
            "js": self.js(data)
        }, self.triggers, []
