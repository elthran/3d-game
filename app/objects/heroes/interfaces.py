from abc import ABC, abstractmethod


class MutationInterface(ABC):
    @abstractmethod
    def add_abilities(self):
        pass

    @abstractmethod
    def update_attributes(self):
        pass
