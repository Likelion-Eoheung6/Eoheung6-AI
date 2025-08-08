from abc import ABC, abstractmethod, ABCMeta
from enum import Enum, EnumMeta

class ABCEnumMeta(EnumMeta, ABCMeta):
    pass
class Basic(Enum, metaclass = ABCEnumMeta):
    pass

class BaseResponseCode(ABC):
    
    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def http_status(self) -> int:
        pass

    @property
    @abstractmethod
    def message(self) -> str:
        pass