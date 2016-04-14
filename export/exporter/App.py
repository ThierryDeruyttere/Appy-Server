from pybars import Compiler
compiler = Compiler()
from .Button import Button
from .List import List
from .Image import Image
from .Textbox import Textbox
from .Label import Label
import json

from export.utils import readFile

componentsClass = {
    "List": List,
    "Button": Button,
    "Textbox": Textbox,
    "Image": Image,
    "Label": Label
}

def _json(self, context):
    return json.dumps(context)

helpers = {'json': _json}

class App:

    def __init__(self, appData):
        self.html = compiler.compile(readFile("export/templates/HTML/app_page.html"))
        self.comps = self.createComponents(appData['components'])
        self.info = appData["info"]

    def generate(self):
       app = {
            'components': {},
            'watch': {},
            'genItems': {}
       }
       app["info"] = self.info


       for comp in self.comps:
           compName, compDict, isList = comp.generate()
           if isList:
               app["genItems"][compName] = compDict["genItems"]

           app["components"][compName] = compDict

       print(self.html(app, helpers=helpers))
       return self.html(app, helpers=helpers)

    def createComponents(self, components):
        comps = []
        for componentName in components:
            component = components[componentName]
            compType = component['type']
            comps.append(componentsClass[compType](componentName, component))
        return comps
