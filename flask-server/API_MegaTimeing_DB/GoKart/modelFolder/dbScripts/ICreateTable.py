from abc import abstractmethod, ABC

class ICreateTable(ABC):
    @abstractmethod
    def createTable() -> None:
        raise NotImplementedError