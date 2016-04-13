import sys
import json
import copy
from pybars import Compiler
compiler = Compiler()

def _json(self, context):
    return json.dumps(context)

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

helpers = {'json': _json}

appTemplate = compiler.compile(readFile("export/templates/HTML/app_page.html"))

# def setTriggerBinding(func):
#     for t in func['triggers']:
#         trigger = app_description['logic']['triggers'][t['name']]
#         component = app_description['components'][trigger['component']]
#         component['binding'][trigger['action']] = func['name']

# def readList(List):
#     for comp in List['properties']['items']:
#         print(comp)
#         name = comp.name
#         print(name)
#         print(comp.components)
#         for item in comp.components:
#             print(item)

def processComponent(name, component):
    # Set component bindings
    setComponentBindings(name, component)

    # Set html for that component
    if type(templates[component['type']]).__name__ == "function":
        component['html'] = templates[component['type']](component['binding'])
        # print(json.dumps(component, indent=2))
        app_data['components'][name] = component

        # If our component is a list we need to check inside the list for elements
        if component['type'] == 'List':
            app_data['lists'][name] = {
                'itemcomponent': name.lower() + '_component'
            }

            app_data['lists'][name]['components'] = {}
            app_data['lists'][name]['html'] = ''
            for list_component in component['properties']['newItemComponents']:
                setComponentBindings(list_component['name'], list_component)
                app_data['lists'][name]['components'][list_component['name']] = list_component
                app_data['lists'][name]['html'] += templates[list_component['type']](list_component['binding'])

    else:
        component['html'] = None


def setComponentBindings(name, component):
    component['binding'] = {}

    # Set the binding for each property to the correct object in the data
    # so the html can be properly instantiated
    # e.g. "name" -> "components.Button0.name"
    for property_name, property_obj in component['properties'].items():
        if 'input' in property_obj:
            app_data['watch'][name + '.' + property_name] = property_obj['input']

        component['binding'][property_name] = 'components.' + name + '.' + property_name

        if 'value' in property_obj:
            property_obj = property_obj['value']

    # If the component is a list, set the name for the list items as well
    if component['type'] == "List":
        component['binding']["itemcomponent"] = name + "_component"


def export(path):
    app_description = None
    app_description = json.load(open(path, 'r'))


    # app_description = parseProperties(app_description)
    app_description['logic']['methods'] = {}

    # Logic
    # for f in app_description['logic']['functions']:
    #     func = app_description['logic]']['functions'][f]
    #
    #     func['parameters']['name'] = f
    #     func['js'] = templates[func['type']](f)
    #
    #     if len(func['triggers']) > 0:
    #         func['name'] = f + '_method'
    #         app_description['logic']['methods'][func['name']] = func['js']
    #         del app_description['logic']['functions'][f]
    #
    #         # Set the component binding to the right function
    #         setTriggerBinding(func)
    #     else:
    #         func.name = f + '_computed'
    #
    #     # Set all outputs of this logic component to null
    #     app_description['components'][f] = {}
    #     app_description['components'][f]['properties'] = {'result': None}

    # Pages
    # if 'pages' not in app_description:
    #     app_description['pages'] = {}
    #     for pageName in app_description['info']['pageNames']:
    #         app_description['pages'][pageName] = {}
    #         app_description['pages'][pageName]['components'] = {}

    # Components
    for componentName in app_description['components']:
        component = app_description['components'][componentName]
        processComponent(componentName, component)

    # TODO pages
    # if 'page' in component['properties']:
    #     app_description['pages'][component['properties']['page']]['components'][comp] = component

    print(json.dumps(app_data, indent=2))

    # Write HTML output to file
    # console.log(appTemplate(app_description));
    path_array = path.split(".")
    f = open(path_array[0] + ".html", 'w')
    f.write(appTemplate(app_data, helpers=helpers))

app_data = {
    'components': {},
    'watch': {},
    'lists': {}
}

if __name__ == "__main__":
    if sys.argv[1]:
        export(sys.argv[1])
