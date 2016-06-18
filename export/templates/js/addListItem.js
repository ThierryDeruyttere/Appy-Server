function() {
  this.index += 1;
  new_item = {
    index: this.index,
    data: {{{json default_data }}}
  }
  {{#each inputs}}
  new_item.data["{{out_component}}"].{{out_data}} = this.components.{{in_data}}
  {{/each}}

  this.components.{{list}}.genitems.push(new_item);
}
