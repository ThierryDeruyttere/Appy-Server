function() {
  this.index += 1;
  new_item = {
    index: this.index
    data: {{default_data}}
  }
  {{#each inputs}}
  new_item[{{out_component}}].{{out_data}} = {{in_data}}
  {{/each}}

  this.{{list}}.genitems.append(new_item);
}
