from abc import ABCMeta,abstractmethod


class ViewInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_data') and
                callable(subclass.get_data) and
                hasattr(subclass, 'display') and
                callable(subclass.display))

    @abstractmethod
    def get_data(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def display(self):
        raise NotImplementedError
