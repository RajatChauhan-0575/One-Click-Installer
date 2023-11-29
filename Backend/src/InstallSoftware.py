from Logging import writeLog
from RemoteOperations import *
from InstalledSoftware import isSoftwareInstalled
from DatabaseAccessor import DatabaseAccessor
import os


def HandleInstallSoftware(config):
    # Read from config file
    databasePath = config.getDataBasePath()
    localPath = config.getLocalPath()

    print("\n                   Repository List                  ")
    while True:
        try:
            dbAccessor = DatabaseAccessor(databasePath)
        except:
            print("Unable to parse the database")
            input("Press any key to Exit")
            quit()

        count = 1
        teamList = dbAccessor.getListOfTeams()

        for team in teamList:
            print(str(count) + ". " + team)
            count += 1

        print("Press q to exit")
        response = input("Enter the reponse : ")

        if response == "q":
            break

        if int(response) < count:
            # Get the list of software for that team
            count = 1
            softwareList = dbAccessor.getListOfSoftwaresForTeam(
                teamList[int(response) - 1]
            )
            for software in softwareList:
                print(str(count) + ". " + software)
                count += 1

        setting = InstallSoftware.Settings()
        setting.teamName = teamList[int(response) - 1]
        setting.localDownloadPath = localPath
        setting.listOfSoftwares = dbAccessor.getListOfSoftwaresForTeamWithInfo(
            teamList[int(response) - 1]
        )

        installSoftwareInstance = InstallSoftware(setting)
        installSoftwareInstance.startInstallation()


class InstallSoftware:
    class Settings:
        def __init__(self):
            self.teamName = ""
            self.listOfSoftwares = []
            self.localDownloadPath = ""

    def __init__(self, setting):
        self.setting = setting

    def getInstallargs(self, softName):
        args = ""
        softwareList = self.setting.listOfSoftwares

        for software in softwareList:
            if software["name"] is softName:
                args = software["install_args"]
                break

        return args

    def install(self, localpath, name):
        args = ""
        args = self.getInstallargs(name)
        installCommand = ""

        if not bool(args):
            print("No install args found...")
            return
        else:
            installCommand = localpath + " " + args
            print(installCommand)

        try:
            subprocess.Popen(
                installCommand, stdout=subprocess.PIPE, shell=True
            ).communicate()
        except:
            print("could not install : " + name + " Please try manual Installation")

    def initilize(self):
        # Create local path dir
        localPath = self.setting.localDownloadPath
        exists = os.path.exists(localPath)

        if not exists:
            os.makedirs(localPath)
        else:
            writeLog("Dir already exists")

    def startInstallation(self):
        """Logic to download software and keep it in local
        directory mentioned in localPath"""

        progress = 0
        bar = "\\"

        self.initilize()

        downloadedSoftwares = downloadSoftwaresFomURL(
            self.setting.listOfSoftwares, self.setting.localDownloadPath
        )

        if downloadedSoftwares == None:
            return

        segment = int(100 / len(downloadedSoftwares))

        for softName, filePath in downloadedSoftwares.items():
            bar = "/" if bar == "\\" else "\\"
            print("Installation Progress : " + str(progress) + "%" + "....." + bar)

            progress += segment

            print("Installing Software : " + softName + "\n")

            if not isSoftwareInstalled(softName):
                self.install(filePath, softName)
            else:
                print("Software already installed skipping...")
                continue

        print("Software Installation complete....\n")
