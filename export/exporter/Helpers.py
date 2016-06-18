import json

def _json(self, context):
    return json.dumps(context)

helpers = {'json': _json}