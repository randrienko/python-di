import inspect
from pydi.exceptions import BeanNotExistException, ClassNotFoundException

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
                
        
        if type(bean["value"]) == str and bean["value"].index("class_path:") == 0:
            class_path = bean["value"][11:]
            bean["value"] = self._get_class(class_path)
            
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
    
    def _get_class(self, class_path):
        parts = class_path.split('.')
        module = ".".join(parts[:-1])
        try:
            m = __import__( module )
            for comp in parts[1:]:
                m = getattr(m, comp)
        except ImportError:
            raise ClassNotFoundException(class_path)
        
        return m
    
    def get(self, name):
        if name not in self.container and name in self.beans_config:
            d = self._init_default_bean(self.beans_config[name])
            
            if d['scope'] == 'prototype':
                return self._init_instance(d)
            
            self.container[name] = self._init_instance(d)
        if name not in self.container:
            raise BeanNotExistException(name)
        
        return self.container[name]
