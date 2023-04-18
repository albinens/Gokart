from abc import abstractmethod, ABC

class ITableInsertion(ABC):
    @abstractmethod
    def insertIntoTable() -> None:
        raise NotImplementedError