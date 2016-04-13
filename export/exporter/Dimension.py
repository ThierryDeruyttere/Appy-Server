class Dimension:
    def __init__(self, dim):
        self.height = dim["height"]
        self.width = dim["width"]
        self.row = dim["row"]
        self.column = dim["col"]

    def getDict(self):
        return {
            "height": self.height,
            "width": self.width,
            "row": self.row,
            "column": self.column
        }
