from abc import ABC, abstractmethod

class IA(ABC):
    @abstractmethod
    def get_response(self, question):
        pass
