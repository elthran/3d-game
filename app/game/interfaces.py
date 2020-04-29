from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def tool_belt_update(self, game, operation, key, hero, time_delta):
        pass
