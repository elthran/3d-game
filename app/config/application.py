import os

class Application:
    ROOT = os.getcwd()

    @classmethod
    def root(cls, path=''):
        return os.path.join(cls.ROOT, path)
