from datetime import date
import os

global fileObject
global logpath


def initializeLogReport(path):
    global logpath
    logpath = os.path.join(path, "Installlog" + str(date.today()) + ".txt")
    try:
        exist = os.path.exists(path)

        if not exist:
            os.makedirs(path)

        # os.mkdir(logPath)
        open(logpath, "x")
    except:
        pass

    global fileObject
    fileObject = open(logpath, "w")
    fileObject.truncate()


def writeLog(logData):
    global fileObject
    fileObject.write(logData + "\n")
    fileObject.flush()


def closeLogfile():
    global fileObject
    fileObject.close()


def openLogFile():
    global logpath
    os.startfile(logpath)


# Test Logging code
if __name__ == "__main__":
    path = r"C:\\Temp\\software"
    initializeLogReport(path)
    writeLog("test")
    closeLogfile()
    openLogFile()
