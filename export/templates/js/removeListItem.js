function(el) {
  var containing_element = $(el).closest("{{elemclass}}");
  // Option 1: JQuery.index()
  var idx = containing_element.index();
  // option 2: data- attribute
  // var idx = containing_element.data("...");

  this.{{list}}.genitems.splice(idx, 1);
}
