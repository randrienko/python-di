import inspect

from six import string_types

from pydi.exceptions import BeanNotExistException, WrongValueException
from pydi.functions import get_class
from pydi.parsers import *


class BeansContainer:
    def __init__(self):
        self.beans_config = dict()
        self.default_bean = {
            "value": "",
            "scope": "singleton",
            "args": [],
            "properties": {},
            "lazy": False
        }

        self._bean_parser = BeanNameParser()
        self._class_path_parser = ClassPathParser()

        self.container = dict()
           
    def init_beans(self, beans_config):
        self.beans_config = beans_config
        for name in self.beans_config.keys():
            self._init_bean(name)

    def _init_bean(self, name):
        bean = self.beans_config[name]

        d = self._init_default_bean_data(bean)
        if d["scope"] == "singleton" and not d["lazy"]:
            self.container[name] = self._activate_bean(d)
            
    def _init_default_bean_data(self, bean):
        for k, v in self.default_bean.items():
            if k not in bean:
                bean[k] = v
        return bean
    
    def _activate_bean(self, bean):
        """
        If the value type is class then value return.
        If the value type is string wit class path then class imports and return.
        """

        if self._class_path_parser.is_class_path(bean["value"]):
            class_path = self._class_path_parser.parse_class_path(bean["value"])
            instance = self._get_instance(get_class(class_path), bean["args"], bean["properties"])

        elif self._bean_parser.is_bean(bean["value"]):
            bean_name = self._bean_parser.parse_bean_name(bean["value"])
            instance = self.get(bean_name)
        else:
            raise WrongValueException(bean['value'])

        return instance

    def _get_instance(self, class_definition, args=[], properties={}):
        # set arguments for __init_ method
        _args = []
        for arg in args:
            if self._bean_parser.is_bean(arg):
                bean_name = self._bean_parser.parse_bean_name(arg)
                _args.append(self.get(bean_name))
            else:
                _args.append(arg)

        instance = class_definition(*_args)

        # initialize object properties
        for k, v in properties.items():
            if self._bean_parser.is_bean(v):
                bean_name = self._bean_parser.parse_bean_name(v)
                property_value = self.get(bean_name)
            else:
                property_value = v

            instance.__dict__[k] = property_value

        return instance

    def get(self, name):
        if name not in self.container and name in self.beans_config:
            d = self._init_default_bean_data(self.beans_config[name])
            
            if d['scope'] == 'prototype':
                return self._activate_bean(d)
            
            self.container[name] = self._activate_bean(d)
        if name not in self.container:
            raise BeanNotExistException(name)
        
        return self.container[name]
