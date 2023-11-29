import winapps


def isSoftwareInstalled(softname):
    installedsoftwares = [item.name for item in winapps.list_installed()]
    return softname in installedsoftwares if True else False


def listInstalledSoftwares():
    for item in winapps.list_installed():
        print(item.name)
