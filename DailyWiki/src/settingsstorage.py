"""Implementation of the module used to store and retrieve user settings, here
in a configuration file. It also handles OS-specific operations such as editing
the Windows registry"""

import logging
import platform
from pathlib import Path
from configparser import ConfigParser
import os
import os.path
import winreg

from settingsstorageinterface import SettingsStorageInterface


class SettingsStorage(SettingsStorageInterface):

    def __init__(self):

        self.logger = logging.getLogger(__name__)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log',
                                                  maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)

        self.config = ConfigParser()
        self.readConfigFile()


    def getSettings(self):

        self.readConfigFile()
        return_dict = {}

        if self.config["GENERAL"]["RANDOM"] == "True":

            return_dict["RANDOM"] = True

        else:

            return_dict["RANDOM"] = False

        if self.config["GENERAL"]["AUTOLAUNCH"] == "True":

            return_dict["AUTOLAUNCH"] = True

        else:

            return_dict["AUTOLAUNCH"] = False

        return_dict["TOPICS"] = []

        if "TOPICS" in self.config:

            for i in self.config["TOPICS"]:

                return_dict["TOPICS"].append(self.config["TOPICS"][i])


        return return_dict

    def saveSettings(self, settings):

        self.config["GENERAL"]["RANDOM"] = str(settings["RANDOM"])
        self.config["GENERAL"]["AUTOLAUNCH"] = str(settings["AUTOLAUNCH"])

        current_topics = self.config.options("TOPICS")
        new_topic_index = len(current_topics)

        self.config["TOPICS"] = {}

        for i in settings["TOPICS"]:

            self.config["TOPICS"][str(new_topic_index)] = i
            new_topic_index += 1

        if not self.setAutolaunch(settings["AUTOLAUNCH"]):

            return False

        with open("conf/settings.ini", 'w') as configfile:

            self.config.write(configfile)
    
        return True

    def createDefaultConfigFile(self):

        self.config["GENERAL"] = {"RANDOM" : True,
                                  "AUTOLAUNCH" : True}

        self.config["TOPICS"] = {}

        with open("conf/settings.ini", 'w') as configfile:

            self.config.write(configfile)
            configfile.close()

    def readConfigFile(self):

        self.logger.debug("Reading configuration file")

        if os.path.isfile("conf/settings.ini"):

            self.config.read("conf/settings.ini")


            if ("GENERAL" in self.config and "RANDOM" in self.config["GENERAL"] and "AUTOLAUNCH" in self.config["GENERAL"] and
            (self.config["GENERAL"]["RANDOM"] == "True" or self.config["GENERAL"]["RANDOM"] == "False") or
            (self.config["GENERAL"]["AUTOLAUNCH"] == "True" or self.config["GENERAL"]["AUTOLAUNCH"] == "False")):

                return

            else:

                self.logger.warning("Some settings are missing, creating a default configuration file to use instead")
                self.config.remove_section("TOPICS")
                self.config.remove_section("GENERAL")
                os.remove("conf/settings.ini")
                self.createDefaultConfigFile()



        else:

            self.logger.warning("Coud not find the configuration file, creating a default file instead")
            self.createDefaultConfigFile()
    
    def setAutolaunch(self, launch_at_startup):
        

        """This method edits the Windows registry to enable or disable auto-launch
        at startup for DailyWiki. By default, DailyWiki automatically starts
        when the user logs in his Window session"""
            
        if launch_at_startup:
            
            return self.addAutolaunchToWindowsRegistry()
            
        else:
                
            return self.deleteAutolaunchFromWindowsRegistry()

    
    def addAutolaunchToWindowsRegistry(self):

        self.logger.debug("Adding DailyWiki entry in Windows registry")

        path = Path(os.path.dirname(os.path.realpath(__file__)))
        path = path.parent.parent

        exe_name = "DailyWiki.exe"
        address = os.path.join(path, exe_name)
        
        key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
        
        bitness = platform.architecture()[0]


        if bitness == '32bit':
        
            other_view_flag = winreg.KEY_WOW64_64KEY
        
        elif bitness == '64bit':
        
            other_view_flag = winreg.KEY_WOW64_32KEY
            
        try:

            opened_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_value, 0, access=winreg.KEY_ALL_ACCESS | other_view_flag)

        except FileNotFoundError:

            self.logger.error("Unable to open a registry entry for DailyWiki")
            return False

        winreg.SetValueEx(opened_key,"DailyWiki", 0, winreg.REG_SZ, address)    
        winreg.CloseKey(opened_key)


        return True
        
    def deleteAutolaunchFromWindowsRegistry(self):

        self.logger.debug("Removing DailyWiki entry from Windows registry")
        
        key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
        
        path = Path(os.path.dirname(os.path.realpath(__file__)))
        path = path.parent.parent
        exe_name = "DailyWiki.exe"
        address = os.path.join(path, exe_name)


        bitness = platform.architecture()[0]

        if bitness == '32bit':
        
            other_view_flag = winreg.KEY_WOW64_64KEY
        
        elif bitness == '64bit':
        
            other_view_flag = winreg.KEY_WOW64_32KEY

        try:
        
            opened_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_value, 0, access=winreg.KEY_ALL_ACCESS | other_view_flag)
        
        except FileNotFoundError:

            self.logger.error("Unable to find the registry key for DailyWiki")
            return False
        
        except OSError:

            self.logger.debug("The value for DailyWiki does not exist in the registry")
            return True
        
        try:

            winreg.DeleteValue(opened_key, "DailyWiki")

        except:

            self.logger.debug("The value for DailyWiki does not exist in the registry: no changes are made")
            
        winreg.CloseKey(opened_key)

        self.logger.debug("Registry entry removed")

        return True

