#https://www.tutorialspoint.com/spring/spring_bean_bean.htm

import inspect

class BeansContainer:
    def __init__(self):
        self.default_bean = {
            "value": "",
            "scope": "singleton",
            "args": [],
            "lazy": False
        }

        self.container = dict()
       
            
    def init_beans(self, beans_config):
        self.beans_config = beans_config
        for name in self.beans_config.keys():
            self._init_bean(name)

    def _init_bean(self, name):
        bean = self.beans_config[name]
            
        d = self._init_default_bean(bean)
        if d["scope"] == "singleton" and not d["lazy"]:
            self.container[name] = self._init_instance(d)
            
    def _init_default_bean(self, bean):
        for k, v in self.default_bean.items():
            if k not in bean:
                bean[k] = v
                
        try:
            if type(bean["value"]) == str and bean["value"].index("class_path:") == 0:
                class_path = bean["value"][11:]
                bean["value"] = self._get_class(class_path)
        except ValueError:
            pass
        return bean

    def _init_instance(self, bean_info):

        if inspect.isclass(type(bean_info["value"])):
            args = []
            for arg in bean_info["args"]:
                try:
                    if type(arg) == str and arg.index("bean:") == 0:
                       arg_bean_name = arg[5:]
                       args.append(self.get(arg_bean_name))
                    else:
                        args.append(arg)
                    
                except ValueError:
                   args.append(arg)
                   
            if type( bean_info["value"]) != str:
                instance = bean_info["value"](*args)
            else:
                instance = bean_info["value"]
        else:
           instance = bean_info["value"]
        return instance
    
    def _get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m
    
    def get(self, name):
        if name not in self.container and name in self.beans_config:
            d = self._init_default_bean(self.beans_config[name])
            
            if d['scope'] == 'prototype':
                return self._init_instance(d)
            
            self.container[name] = self._init_instance(d)
            
        return self.container[name]

# ======================

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Container(metaclass=Singleton):
    _beans_container = BeansContainer()        
        
    @staticmethod
    def start(beans_config):
        Container._beans_container.init_beans(beans_config)
        
    @staticmethod    
    def get(name):
        return Container._beans_container.get(name)
