Handlebars = require('handlebars');
fs = require('fs');
_ = require('underscore');

// Register Handlebars helper to stringify json
// Use: {{{json object}}}
// Source: http://stackoverflow.com/a/10233247
Handlebars.registerHelper('json', function(context) {
    return JSON.stringify(context);
});

// To test this file you can just run "node exporter.js file"
// Add new templates here
var templates = {
  Button: Handlebars.compile(fs.readFileSync("export/templates/HTML/button.html").toString()),
  Image: Handlebars.compile(fs.readFileSync("export/templates/HTML/image.html").toString()),
  Label: Handlebars.compile(fs.readFileSync("export/templates/HTML/label.html").toString()),
  Textbox: Handlebars.compile(fs.readFileSync("export/templates/HTML/textbox.html").toString()),
  List: Handlebars.compile(fs.readFileSync("export/templates/HTML/list.html").toString()),
  Plus: Handlebars.compile(fs.readFileSync("export/templates/js/plus.js").toString()),
  GotoPage: Handlebars.compile(fs.readFileSync("export/templates/js/gotopage.js").toString()),
  AddTextToList: Handlebars.compile(fs.readFileSync("export/templates/js/addTextToList.js").toString()),
}

var appTemplate = Handlebars.compile(fs.readFileSync("export/templates/HTML/app_page.html").toString());

function parseProperties(appDescription) {
  for(comp in appDescription.components) {
    appDescription.components[comp].binding = {};
    for(prop in appDescription.components[comp].properties) {
      // Set bindings between properties
      if(appDescription.components[comp].properties[prop].input) {
        appDescription.watch[comp + '.' + prop] = appDescription.components[comp].properties[prop].input;
      }

      appDescription.components[comp].binding[prop] = 'components.' + comp + '.properties.' + prop;

      if( appDescription.components[comp].properties[prop].value)
        appDescription.components[comp].properties[prop] = appDescription.components[comp].properties[prop].value;

    }
  }
  return appDescription
}

function setTriggerBinding(func) {
  func.triggers.forEach(function(t) {
    var trigger = appDescription.logic.triggers[t.name];
    var component = appDescription.components[trigger.component];

    component.binding[trigger.action] = func.name;
  });
}

function readList(List, appDescription){
  console.log(List.properties.items);
  for(comp in List.properties.items){
    console.log(comp);
    var name = comp.name;
    console.log(name);
    console.log(comp.components);
    for(item in comp.components){
      console.log(item);
    }
  }

}


// Read json file
if(process.argv[2]) {
  var appDescription = JSON.parse(fs.readFileSync(process.argv[2]).toString());
  appDescription.watch = {};
  appDescription = parseProperties(appDescription);
  appDescription.logic.methods = {};

  // Logic
  for(f in appDescription.logic.functions) {

    func = appDescription.logic.functions[f];

    func.js = templates[func.type](_.extend(func.parameters, {'name': f}));

    if(func.triggers.length > 0) {
      func.name = f + '_method';
      appDescription.logic.methods[func.name] = func.js;
      delete appDescription.logic.functions[f];

      // Set the component binding to the right function
      setTriggerBinding(func);
    } else {
      func.name = f + '_computed';
    }

    // Set all outputs of this logic component to null
    appDescription.components[f] = {};
    appDescription.components[f].properties = {result: null};
  }

  // Pages
  appDescription.pages = appDescription.pages || {};
  appDescription.info.pageNames.forEach(function(pageName) {
    appDescription.pages[pageName] = {}
    appDescription.pages[pageName].components = {}
  });

  // Components
  for(comp in appDescription.components) {
    component = appDescription.components[comp];

    // TODO: if we change this to coffeescript:
    // component.html = templates[component.type]?(component.binding);
    // Set html for that component
    if(typeof templates[component.type] === "function"){
      component.html =  templates[component.type](component.binding);

      // If our component is a list we need to check inside the list for elements
      if(component.type == "List"){
       console.log(component);
        readList(component, appDescription)
      }

    }else{
       component.html = void 0;
    }

    if(component.properties.page) {
      appDescription.pages[component.properties.page].components[comp] = component;
    }
  }

  //Write HTML output to file
  //console.log(appTemplate(appDescription));
  var path_array = process.argv[2].split(".");
  fs.writeFileSync(path_array[0]+".html", appTemplate(appDescription))
}
else {
  console.log("no input file");
}
