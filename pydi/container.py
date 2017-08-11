from pydi.di import BeansContainer

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Container(metaclass=Singleton):
    _beans_container = BeansContainer()        
        
    @staticmethod
    def setup(beans_config):
        Container._beans_container.init_beans(beans_config)
        
    @staticmethod    
    def get(name):
        return Container._beans_container.get(name)