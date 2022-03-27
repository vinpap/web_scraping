from abc import ABC, abstractmethod


# =============================================================================
# !!!! INTERFACE, DO NOT TRY TO INSTANTIATE
# Defines a generic interface for the subsystem responsible for handling how the
# settings are stored, as well as editing Windows registry
# =============================================================================


class SettingsStorageInterface(ABC):

    @abstractmethod
    def getSettings(self):

        pass

    @abstractmethod
    def saveSettings(self, settings):

        pass
