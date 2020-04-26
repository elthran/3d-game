from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def update(self, operation, key, hero, time_delta):
        pass
