import json


class DatabaseAccessor:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        with open(self.filename) as file:
            self.data = json.load(file)

    def save(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def getListOfTeams(self):
        teams = []
        keys = self.data.keys()

        for key in keys:
            teams.append(key)

        return teams

    def getListOfSoftwaresForTeam(self, teamName):
        softwareList = []

        for software in self.data[teamName]:
            name = software["name"]
            softwareList.append(name)

        return softwareList

    def getListOfSoftwaresForTeamWithInfo(self, teamName):
        softwareList = []

        for software in self.data[teamName]:
            softwareList.append(software)

        return softwareList


# def set(self, key, value):
#     self.data[key] = value
#     self.save()

# def delete(self, key):
#     del self.data[key]
#     self.save()
