"""This module reads the settings it is provided and check their validity."""

import logging

from settingsreaderinterface import SettingsReaderInterface

class SettingsReader(SettingsReaderInterface):

    def __init__(self, settings_storage):

        self.logger = logging.getLogger(__name__)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log',
                                                  maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)

        self.settings_storage = settings_storage

    def readSettings(self):

        settings = self.settings_storage.getSettings()

        if (not settings
                or "RANDOM" not in settings
                or "TOPICS" not in settings
                or "AUTOLAUNCH" not in settings
                or not isinstance(settings["RANDOM"], bool)
                or not isinstance(settings["TOPICS"], list)
                or not isinstance(settings["AUTOLAUNCH"], bool)
                ):

            self.logger.warning("The settings provided do not follow the right format. Using default settings instead")
            return self.getDefaultSettings()


        for i in settings["TOPICS"]:

            if not isinstance(i, str):

                self.logger.warning("The settings provided do not follow the right format. Using default settings instead")
                return self.getDefaultSettings()

        return {"RANDOM" : settings["RANDOM"],
                "TOPICS" : settings["TOPICS"],
                "AUTOLAUNCH" : settings["AUTOLAUNCH"]}

    def getDefaultSettings(self):

        return {"RANDOM" : True,
                "TOPICS" : [],
                "AUTOLAUNCH" : True}
