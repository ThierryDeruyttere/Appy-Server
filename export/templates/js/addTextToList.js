function() {
  var size = this.{{list}}.length + 1000;

  var obj = {
    "index": size,
    "name": "item_"+size,
    "message": {
      "name": "Text",
      "type": "text",
      "value": this.{{text}}
    },
    "visible": {
    "type": "switch",
        "value": true
    }
  }

  this.{{list}}.push(obj);
  return null;
}
