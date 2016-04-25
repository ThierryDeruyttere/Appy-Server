function() {
  new_item = {{default_item}}
  {{#each inputs}}
  new_item[{{out_component}}].{{out_data}} = {{in_data}}
  {{/each}}

  this.{{list}}.genitems.append(new_item);
}
