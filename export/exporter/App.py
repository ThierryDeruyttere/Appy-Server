from pybars import Compiler
compiler = Compiler()
from export.exporter.components.Components import componentsClass
from export.exporter.functions.Functions import functionClass
from export.exporter.Trigger import Trigger
from export.exporter.components.Dimension import Dimension
import json

from export.utils import readFile

def _json(self, context):
    return json.dumps(context)

helpers = {'json': _json}

class App:

    def __init__(self, appData):
        self.html = compiler.compile(readFile("export/templates/HTML/app_page.html"))
        Dimension.setAppDims(appData["info"]["width"], appData["info"]["height"])
        self.comps = self.createComponents(appData['components'])
        self.info = appData["info"]
        self.functions = self.createFunctions(appData["logic"]["functions"])
        self.triggers = self.createTriggers(appData["logic"]["triggers"])

    def generate(self):
        app = {
            'components': {},
            'watch': {},
            'genItems': {},
            'logic': {"functions": {}, "methods": {}}
        }
        app["info"] = self.info

        for function in self.functions:
            f, triggers = function.generate()
            app["logic"]["functions"][f["name"]] = f

            # Change triggers
            for t in triggers:
                if t not in self.triggers:
                    raise Exception("Gave wrong trigger!")

                self.triggers[t]["functions"] += [f["name"]]


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

    def createFunctions(self, functions):
        funcs = []
        for name, function in functions.items():
            funcType = function["type"]
            print(name, function)
            funcs.append(functionClass[funcType](name, function))
        return funcs

    def createTriggers(self, triggers):
        triggers = {}
        for name, info in triggers.items():
            triggers[name] = {
                "functions": [],
                "component": info["component"],
                "action": info["action"]
            }
        return triggers
