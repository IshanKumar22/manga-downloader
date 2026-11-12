from abc import ABC, abstractmethod


class Chapter(ABC):
    def __init__(self, url):
        self.url = url
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def get_pages(self) -> tuple[str]:
        pass
    
    def __repr__(self):
        return f"Chapter<{self.url}>"
    
    def __str__(self):
        return f"Chapter<{self.url}>"

class Series(ABC):
    def __init__(self, url):
        self.url = url
    
    @abstractmethod
    def get_chapters(self) -> list[Chapter]:
        pass
    
    def __repr__(self):
        return f"Series<{self.url}>"
    
    def __str__(self):
        return f"Series<{self.url}>"

class Source(ABC):
    @property
    @abstractmethod
    def url(self):
        pass
    
    @classmethod
    @abstractmethod
    def search_series(self, query: str) -> list[Series]:
        pass
    
    @classmethod
    @abstractmethod
    def get_series(self, slug: str) -> Series:
        pass
