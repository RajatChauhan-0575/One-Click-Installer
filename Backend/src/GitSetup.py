from InstalledSoftware import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from JsonReader import *


def HandleGitSetup(config):
    if not isSoftwareInstalled("Git"):
        print("Please install git before configuring...")
        return

    sshFilePath = config.getSSHDataPath()
    jsonReader = JsonReader(sshFilePath)

    name = input("Please enter username for commit: ")
    emailid = input("Please enter the email id for commit: ")
    passwd = ""

    setting = GitSetup.Settings()
    setting.systemUser = os.getlogin()
    setting.sshFileTemplateData = jsonReader.getData("Data")
    setting.configFilePath = (
        "C:\\Users\\" + setting.systemUser + r"\SSHTest" + r"\.ssh" + r"\config"
    )
    setting.gerritEmailId = emailid
    setting.gerritUserName = name
    setting.gerritPwd = passwd

    setup = GitSetup(setting)
    setup.gitSetup()


class GitSetup:
    class Settings:
        def __init__(self):
            self.sshFileTemplateData = ""
            self.systemUser = ""
            self.configFilePath = ""
            self.gerritUserName = ""
            self.gerritEmailId = ""
            self.gerritPwd = ""  # Need to deal with how to store password

    def __init__(self, setting):
        self.setting = setting

    def initialize(self):
        sshpath = self.setting.configFilePath.split(".ssh")[0] + "//.ssh"

        if not os.path.exists(sshpath):
            os.makedirs(sshpath)
        else:
            print("SSH folder already exists...")

    def setConfigFile(self):
        # Add configs
        try:
            open(self.setting.configFilePath, "x")
        except:
            print("Config file already exists....")

        filewriter = open(self.setting.configFilePath, "w")

        for data in self.setting.sshFileTemplateData:
            if data == "User ":
                data = data + self.setting.systemUser
            filewriter.writelines(data + "\n")

        print("Config file generated...")

        os.system(f"git config --global user.name { self.setting.gerritUserName }")
        os.system(f"git config --global user.email { self.setting.gerritEmailId }")

    def generateSSHKey(self):
        os.system(f"ssh-keygen -t rsa -C { self.setting.gerritEmailId }")
        path = r"C:\Users\\" + self.setting.systemUser + r"\.ssh\id_rsa.pub"

        with open(path, "rb") as sshfile:
            sshkey = sshfile.read()

        key = str(sshkey, "UTF-8")
        print("Your ssh key: " + key)

        return key

    def setSSHKeyOnGerrit(self, sshkey):
        try:
            driver = webdriver.Chrome("chromedriver")
            driver.get(r"http://gerrit-git.amd.com/login/")
            driver.implicitly_wait(15)

            loginBox = driver.find_element(by=By.NAME, value="username")
            loginBox.send_keys(self.setting.systemUser)

            pwdBox = driver.find_element(by=By.NAME, value="password")
            pwdBox.send_keys(self.setting.gerritPwd)

            signinButton = driver.find_elements(by=By.ID, value="b_signin")
            signinButton[0].click()

            print("Login Successful...!!")

            driver.get(r"http://gerrit-git.amd.com/settings/#SSHKeys")
            time.sleep(1)
            selector = r'document.querySelector("gr-app").shadowRoot.querySelector("gr-app-element").shadowRoot.querySelector("gr-settings-view").shadowRoot.querySelector("gr-ssh-editor").shadowRoot.querySelector("iron-autogrow-textarea").shadowRoot.querySelector("div.textarea-container.fit")'

            shadow_section = self.getShadowDOMElement(driver, selector)
            sshTextArea = shadow_section.find_element(by=By.ID, value="textarea")
            sshTextArea.send_keys(sshkey)
            selector = r'document.querySelector("gr-app").shadowRoot.querySelector("gr-app-element").shadowRoot.querySelector("gr-settings-view").shadowRoot.querySelector("gr-ssh-editor").shadowRoot.querySelector("#addButton")'
            submit = self.getShadowDOMElement(driver, selector)

            submit.click()

            driver.quit()
            print("SSH key added successfully...!!")
        except:
            print("Login Failed")

    def getShadowDOMElement(self, driver, selector):
        running_script = f"return {selector}"
        element = driver.execute_script(running_script)
        return element

    def gitSetup(self):
        self.initialize()
        self.setConfigFile()

        sshkey = self.generateSSHKey()
        self.setSSHKeyOnGerrit(sshkey)
