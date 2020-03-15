import os

from app.config.initializers import *

class Application:
    ROOT = os.getcwd()

    @classmethod
    def root(cls, path=''):
        return os.path.join(cls.ROOT, path)

loadPrcFile('app/config/Config.prc')
