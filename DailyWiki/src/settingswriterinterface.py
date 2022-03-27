from abc import ABC, abstractmethod

# =============================================================================
# !!!! INTERFACE, DO NOT TRY TO INSTANTIATE
# Defines a generic interface for the subsystem responsible for writing the
# settings. It does not depend on any technical considerations (e.g. how and
# where the settings are stored)
# =============================================================================

class SettingsWriterInterface(ABC):
    
    @abstractmethod
    def saveSettings(self, settings):

        pass
    
