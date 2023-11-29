import json


class ConfigReader:

    __configInstance = None

    def __init__(self, filePath):
        if ConfigReader.__configInstance != None:
            raise Exception("This is a singleton Class")
        else:
            with open(filePath) as file:
                self.data = json.load(file)

            ConfigReader.__configInstance = self

    @staticmethod
    def getInstance(filePath):
        if ConfigReader.__configInstance == None:
            ConfigReader(filePath)

        return ConfigReader.__configInstance

    def getDataBasePath(self):
        return self.__fetchPath("DataBase")

    def getChromePath(self):
        return self.__fetchPath("Chrome")

    def getLocalPath(self):
        return self.__fetchPath("Local")

    def getLogPath(self):
        return self.__fetchPath("Log Path")

    def getSSHDataPath(self):
        return self.__fetchPath("Git ssh")

    def getBookmarkPath(self):
        return self.__fetchPath("bookmarks")

    def __fetchPath(self, name):
        return self.data[name]
