import sys
import json
from pybars import Compiler
compiler = Compiler()

def readFile(filePath):
    f = open(filePath, 'r')
    return f.read()

templates = {
  'Button': compiler.compile(readFile("export/templates/HTML/button.html")),
  'Image': compiler.compile(readFile("export/templates/HTML/image.html")),
  'Label': compiler.compile(readFile("export/templates/HTML/label.html")),
  'Textbox': compiler.compile(readFile("export/templates/HTML/textbox.html")),
  'List': compiler.compile(readFile("export/templates/HTML/list.html")),
  'Plus': compiler.compile(readFile("export/templates/js/plus.js")),
  'GotoPage': compiler.compile(readFile("export/templates/js/gotopage.js")),
  'AddTextToList': compiler.compile(readFile("export/templates/js/addTextToList.js")),
}
appTemplate = compiler.compile(readFile("export/templates/HTML/app_page.html"))

def parseProperties(appDescription):
  for comp in appDescription.components:
    appDescription.components[comp].binding = {}
    for prop in appDescription.components[comp].properties:
      # Set bindings between properties
      if(appDescription.components[comp].properties[prop].input) :
        appDescription.watch[comp + '.' + prop] = appDescription.components[comp].properties[prop].input

      appDescription.components[comp].binding[prop] = 'components.' + comp + '.properties.' + prop

      if( appDescription.components[comp].properties[prop].value):
        appDescription.components[comp].properties[prop] = appDescription.components[comp].properties[prop].value

  return appDescription


def setTriggerBinding(func) :
    for t in func.triggers:
        trigger = appDescription.logic.triggers[t.name]
        component = appDescription.components[trigger.component]
        component.binding[trigger.action] = func.name




# Read json file
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        appDescription = json.load(readFile(args[2]))
        appDescription.watch = {}
        appDescription = parseProperties(appDescription)
        appDescription.logic.methods = {}

        # Logic
        for f in appDescription.logic.functions:
            func = appDescription.logic.functions[f]
            func.parameters['name'] = f
            func.js = templates[func.type]()

            if func.triggers.length > 0 :
              func.name = f + '_method'
              appDescription.logic.methods[func.name] = func.js
              del appDescription.logic.functions[f]

              # Set the component binding to the right function
              setTriggerBinding(func)
            else:
              func.name = f + '_computed'


            # Set all outputs of this logic component to null
            appDescription.components[f] = {}
            appDescription.components[f].properties = {'result': None}


            # Pages
            appDescription.pages = appDescription.pages
            if appDescription.pages is None:
                appDescription.pages = {}
                for pageName in appDescription.info.pageNames:
                    appDescription.pages[pageName] = {}
                    appDescription.pages[pageName].components = {}


            # Components
            for comp in appDescription.components :
                component = appDescription.components[comp]

                #// Set html for that component
                if type(templates[component.type]) == "function":
                    component.html =  templates[component.type](component.binding)

                    #If our component is a list we need to check inside the list for elements
                    if component.type == "List":
                        print(component)
                        #readList(component, appDescription)

                else:
                    component.html = None


                if component.properties.page:
                    appDescription.pages[component.properties.page].components[comp] = component


        #Write HTML output to file
        #console.log(appTemplate(appDescription));
        path_array = args[2].split(".")
        f = open(path_array[0]+".html", 'w')
        f.write(appTemplate(appDescription))

    else:
      print("no input file")

