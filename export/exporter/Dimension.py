class Dimension:
    appWidth = 0
    appHeight = 0

    def __init__(self, dim):
        if "value" in dim:
            dim = dim["value"]

        self.height = dim["height"]
        self.width = dim["width"]
        self.row = dim["row"]
        self.column = dim["col"]

    @staticmethod
    def setAppDims(width, height):
        Dimension.appWidth = width
        Dimension.appHeight = height

    def getDict(self):
        return {
            "height": self.height,
            "width": self.width,
            "row": self.row,
            "column": self.column
        }
