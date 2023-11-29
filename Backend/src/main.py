from pyuac import main_requires_admin
import atexit
from Logging import *
from InstallSoftware import HandleInstallSoftware
from BookmarkSetup import HandleCreateBookMarks
from GitSetup import HandleGitSetup
from InstalledSoftware import listInstalledSoftwares
from GitSetup import HandleGitSetup
import signal
from Config import ConfigReader

# Tasks:
# 1. Copy files from remote to local -- done
# 2. Install Exe - Done
# 3. Install msi - Done
# 4. Install exe and msi with silent options - Done
# 5. Install exe that doesnt take /verysilent arguement - Done
# 6. Create bookmarks - Done
# 7. Git Setup - Done
# 8. Download Latest Build - Done

# P1 issues:
# 1. Multithread download
# 2. Fix Visual studio and postman installation - done
# 3. Fix git issue for fresh system

# P2 issues:
# 1. Fix logging
# 2. Fix new window creation screen
# 3. Download PerfTools and build it
# 4. Reduce requirements from the project
# 5. Local system path not working
# 6. Include a build system

# P3 issues:
# 1. Fix variable names and clean code

# P4 issues:
# 1. Create documentation and present

# Tests:
# 1. Run on fresh desktop


def on_exit():
    closeLogfile()
    openLogFile()
    input("Do you really want to exit ? ")
    print("Exiting app...")


def welcomeScreen():
    print("*****************************************************")
    print("**                                                 **")
    print("**                    Welcome!!                    **")
    print("**                                                 **")
    print("*****************************************************")


@main_requires_admin
def main():
    # signal.signal(signal.SIGTERM, on_exit)

    # writeLog("Inside main")
    # Get the configs
    config = ConfigReader.getInstance("database\\Config.json")

    # Initialize Logger
    initializeLogReport(config.getLogPath())

    welcomeScreen()
    optionsDict = {
        "1.": "Software Installation",
        "2.": "Create Bookmarks",
        "3.": "Git Setup",
        "4.": "Installed softwares",
        "": "Press q to exit...",
    }

    while True:
        print("\n")
        for num, name in optionsDict.items():
            print(num + " " + name)

        res = input("Enter Response : ")

        if res == "q":
            break

        match int(res):
            case 1:
                HandleInstallSoftware(config)
            case 2:
                HandleCreateBookMarks(config)
            case 3:
                HandleGitSetup(config)
            case 4:
                listInstalledSoftwares()
            case default:
                print(r"Enter valid option")

    print("Exiting....")
    closeLogfile()
    openLogFile()
    quit()


if __name__ == "__main__":
    main()
