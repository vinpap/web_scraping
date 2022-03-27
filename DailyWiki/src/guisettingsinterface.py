from abc import ABC, abstractmethod


# =============================================================================
# !!!! INTERFACE, DO NOT TRY TO INSTANTIATE
# Defines a generic interface for the subsystem responsible for managing the
# settings selection dialog window
# =============================================================================

class GuiSettingsInterface(ABC):

    @abstractmethod
    def __init__(self):

        pass

    @abstractmethod
    def displaySettings(self):

        pass
    
