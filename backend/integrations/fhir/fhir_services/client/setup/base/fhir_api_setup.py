from abc import ABC, abstractmethod

class FHIRAPISetup(ABC):
    @abstractmethod
    def get_base_url(self) -> str:
        pass

    @abstractmethod
    def get_session(self):
        pass
