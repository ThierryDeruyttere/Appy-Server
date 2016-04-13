from pybars import Compiler
compiler = Compiler()
from .Button import Button
from .List import List
from .Image import Image
from .Textbox import Textbox
from .Label import Label

from export.utils import readFile

components = {
    "List": List,
    "Button": Button,
    "Textbox": Textbox,
    "Image": Image,
    "Label": Label
}


class App:

    def __init__(self, appData):
        self.html = compiler.compile(readFile("export/templates/HTML/app_page.html"))
        self.comps = self.createComponents(appData['components'])

    def generate(self, appData):
       for comp in self.comps:
           comp.generate()



    def createComponents(self, components):
        comps = []
        for componentName in components:
            component = components[componentName]
            compType = component['type']
            comps.append(components[compType](componentName, component))
        return comps
