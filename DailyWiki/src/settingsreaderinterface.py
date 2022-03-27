from abc import ABC, abstractmethod


# =============================================================================
# !!!! INTERFACE, DO NOT TRY TO INSTANTIATE
# Defines a generic interface for the subsystem responsible for reading the
# settings and checking their validity
# =============================================================================


class SettingsReaderInterface(ABC):

    @abstractmethod
    def readSettings(self):

        pass
    
