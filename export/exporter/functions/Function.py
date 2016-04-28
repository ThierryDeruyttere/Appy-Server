from pybars import Compiler
from export.utils import readFile
from export.exporter.Helpers import helpers
compiler = Compiler()

class Function:
    def __init__(self, name, info):
        self.name = name
        self.triggers = info["triggers"]
        self.params = info["parameters"]
        self.type = info["type"]
        self.outputs = info["outputs"] if "outputs" in info else []

    def generate(self):
        abstract
