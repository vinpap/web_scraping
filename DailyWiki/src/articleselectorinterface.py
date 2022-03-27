from abc import ABC, abstractmethod

# =============================================================================
# !!!! INTERFACE, DO NOT TRY TO INSTANTIATE
# Defines a generic interface for the subsystem responsible for selecting 
# the daily article
# =============================================================================

class ArticleSelectorInterface(ABC):
    
    @abstractmethod
    def getDailyArticleTitle(self):

        pass
    
    @abstractmethod
    def accessDailyArticle(self):
        
        pass