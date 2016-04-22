import json

from pybars import Compiler

from export.exporter.components.Components import componentsClass
from export.exporter.functions.Functions import functionClass
from export.exporter.components.Dimension import Dimension
from export.utils import readFile

compiler = Compiler()

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
            'functionObj': {},
            'logic': {"functions": {}, "methods": {}}
        }
        app["info"] = self.info

        for function in self.functions:
            f, triggers, outputs = function.generate()
            app["logic"]["methods"][f["name"]] = f
            app["functionObj"][function.name] = {output: None for output in outputs}

            for output in function.outputs:
                app["watch"][output] = function.name + outputs[0]

            # Change triggers
            for t in triggers:
                if t not in self.triggers:
                    raise Exception("Gave wrong trigger!")
                self.triggers[t]["functions"] += [f["name"]]

        for comp in self.comps:
            triggerForComp = self.getTriggersFor(comp.name)
            compName, compDict, isList = comp.generate(triggerForComp)
            if isList:
                app["genItems"][compName] = compDict["genItems"]

            app["components"][compName] = compDict

        # print(self.html(app, helpers=helpers))
        return self.html(app, helpers=helpers)

    def getTriggersFor(self, compName):
        triggers = {}
        for name, trigger in self.triggers.items():
            if trigger["component"] == compName:
                triggers[trigger["action"]] = trigger["functions"]

        return triggers

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
        trggers = {}
        for name, info in triggers.items():
            trggers[name] = {
                "functions": [],
                "component": info["component"],
                "action": info["action"]
            }
        return trggers
