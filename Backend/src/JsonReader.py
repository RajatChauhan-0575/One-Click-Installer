import json


class JsonReader:
    def __init__(self, filePath):
        with open(filePath) as file:
            self.data = json.load(file)

    def getData(self, name):
        return self.data[name]
