function(el) {
  var containing_element = $(el).closest(".listItem");
  // Option 1: JQuery.index()
  var idx = containing_element.index();
  // option 2: data- attribute
  // var idx = containing_element.data("...");

  this.components.{{list}}.genitems.splice(idx, 1);
}
