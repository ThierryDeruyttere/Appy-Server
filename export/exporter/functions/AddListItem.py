from .Function import *

class AddListItem(Function):
    def __init__(self, name, info, list):
        Function.__init__(self, name, info)
        self.js = compiler.compile(readFile("export/templates/js/addListItem.js"))
        self.list = list

    def getInputs(self):
        data = []

        for key, input in self.params.items():
            #TODO: Fix out_data...
            data.append({ 'out_component': key,
                  'in_data': input,
                  'out_data': 'text'})

        return data

    def getDefaultData(self):
        data = {}
        for comp in  self.list.newItemComponents:
            data[comp.name] = {}
            for key, prop in comp.props.items():
                if type(prop) is type({}) and "value" in prop:
                    data[comp.name][key] = prop["value"]
                else:
                    data[comp.name][key] = prop
        return data


    def generate(self):
        data = {
            'list': self.outputs[0]['name'],
            'default_data': self.getDefaultData(),
            'inputs': self.getInputs()
        }

        return {
            "name": "method_" + self.name,
            "js": self.js(data, helpers=helpers)
        }, self.triggers, []
