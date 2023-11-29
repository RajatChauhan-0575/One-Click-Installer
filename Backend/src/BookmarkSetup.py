import shutil
import os
from Logging import writeLog


def HandleCreateBookMarks(config):
    settings = CreateBookMark.Settings()
    settings.dataFilePath = config.getBookmarkPath()
    settings.localPath = config.getChromePath()

    bookmarkManager = CreateBookMark(settings)
    bookmarkManager.createBookmarks()


class CreateBookMark:
    class Settings:
        def __init__(self):
            self.localPath = ""
            self.dataFilePath = ""

    def __init__(self, settings):
        self.setting = settings

    def initialize(self):
        if os.path.exists(self.setting.localPath):
            return True
        else:
            return False

    def createBookmarks(self):
        ret = self.initialize()

        if not ret:
            print(
                "Chrome bookmark path is not available, Either chrome is not installed or the path is not accessible...."
            )
        else:
            destDir = self.setting.localPath
            srcDir = self.setting.dataFilePath

            print(destDir + ":" + srcDir)
            shutil.copy(srcDir, destDir)
            writeLog("Bookmarks added successfully !!")
            print("Bookmarks imported..Please restart chrome for booksmarks.")
