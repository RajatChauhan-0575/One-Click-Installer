import subprocess
import codecs
import urllib.request
from jenkinsapi.jenkins import Jenkins
import sys
import os
from shutil import rmtree
import requests


def getRepolist(softwarePath, remotePath):
    ret = subprocess.Popen(
        f"remoteCopy.bat {softwarePath} {remotePath} list_repos ",
        stdout=subprocess.PIPE,
    ).communicate()[0]
    bytelist = ret.split(b"\r\n")
    strlist = []
    for x in bytelist:
        if x != b"":
            strlist.append(codecs.decode(x, "UTF-8"))
    return strlist


def getSoftwarelist(softwarePath, remotePath, repo):
    ret = subprocess.Popen(
        f"remoteCopy.bat {softwarePath} {remotePath} list_softwares {repo}",
        stdout=subprocess.PIPE,
    ).communicate()[0]
    bytelist = ret.split(b"\r\n")
    strlist = []
    for x in bytelist:
        if x != b"":
            strlist.append(codecs.decode(x, "UTF-8"))

    return strlist


def downloadSoftware(softwarePath, remotePath, repo, software):
    ret = subprocess.Popen(
        f"remoteCopy.bat {softwarePath} {remotePath} get_filesFromRemote {repo} {software}",
        stdout=subprocess.PIPE,
    ).communicate()[0]
    return ret


def copyToLocal(softwarePath, remotePath, repo):
    softwares = getSoftwarelist(softwarePath, remotePath, repo)
    print("List of softwares to be Installed : ")
    count = 1
    for software in softwares:
        print(f"{count}. {software}")
        count += 1

    for software in softwares:
        print(f"Downloading : {software}")
        downloadSoftware(softwarePath, remotePath, repo, software)


def getJenkinsBuild(softwarePath):
    try:
        J = Jenkins("http://jenkinserver:8080/")
    except:
        print("Please check your internet connect and connect to VPN..")
        return False, ""

    windowsuprofkeys = []
    for x in J.keys():
        try:
            y = x.split(r"/")[2]
            if len(y) == 20 and x.__contains__(r"AMDuProf_Windows") == True:
                windowsuprofkeys.append(x)
        except:
            continue

    windowsuprofkeys.sort()
    buildVer = windowsuprofkeys[len(windowsuprofkeys) - 1]

    build_ver = J[buildVer].get_last_good_build()

    data = build_ver.name.split(" #")
    ver = data[0].split("-")
    url = f"http://jenkinserver:8080/view/AMDuProf/view/v{ver[1]}/job/{data[0]}/{data[1]}/artifact/AMDuProf-{ver[1]}.{data[1]}.exe"
    folder_path = softwarePath

    try:
        rmtree(folder_path)
    except:
        pass

    try:
        os.makedirs(folder_path)
    except:
        pass

    file_path = folder_path + r"\\" + url.split("/")[-1]

    print("file name : " + file_path)
    u = urllib.request.urlopen(url)
    f = open(file_path, "wb")

    meta = u.info()
    file_size = int(meta["Content-Length"])
    file_size_dl = 0
    block_sz = 8192

    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        spaces = int((file_size_dl / file_size) * 100)

        x = " "
        status = "Download Progress:" + str(spaces) + "%"
        sys.stdout.write("\r" + status)

    print("\nDownload complete ...")
    f.close()

    return True, file_path


def downloadSoftwaresFomURL(softwareList, downloadPath):
    softwareDownloaded = {}

    for software in softwareList:
        softwareName = software["name"]
        urlHasName = software["urlHasName"]
        download_url = software["download_path"]

        softwareDownloadPath = os.path.join(downloadPath, softwareName)
        exist = os.path.exists(softwareDownloadPath)

        if not exist:
            os.mkdir(softwareDownloadPath)

        if urlHasName is True:
            filePath = os.path.join(softwareDownloadPath, download_url.split("/")[-1])
        else:
            fileName = software["fileName"]
            filePath = os.path.join(softwareDownloadPath, fileName)

        print(f"{softwareName} : {download_url}")

        if softwareName == "uprof":
            downloaded, path = getJenkinsBuild(softwareDownloadPath)

            if downloaded:
                softwareDownloaded[softwareName] = path
        else:
            response = requests.get(download_url, stream=True)
            with open(filePath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            softwareDownloaded[softwareName] = filePath

    return softwareDownloaded
