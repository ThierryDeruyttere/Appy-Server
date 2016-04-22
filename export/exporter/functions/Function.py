from pybars import Compiler
from export.utils import readFile

compiler = Compiler()

class Function:
    def __init__(self, name, info):
        self.name = name
        self.triggers = info["triggers"]
        self.params = info["parameters"]
        self.type = info["type"]

    def generate(self):
        abstract
