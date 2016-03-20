function() {
  var size = this.{{list}}.length + 1000;

  var obj = {
    "index": size,
    "name": "item_"+size,
    "message": {
      "name": "Text",
      "type": "text",
      "value": this.{{text}}
    }
  }

  this.{{list}}.push(obj);
  return null;
}
