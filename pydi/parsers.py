
class ClassPathParser(object):
    def __init__(self):
        self._class_path_prefix = "class_path:"

    def is_class_path(self, v):
        try:
            return type(v) == str and v.index(self._class_path_prefix) == 0
        except ValueError:
            pass

    def parse_class_path(self, v):
        position = len(self._class_path_prefix)
        return v[position:]


class BeanNameParser(object):
    def __init__(self):
        self._bean_prefix = "bean:"

    def is_bean(self, v):
        try:
            return type(v) == str and v.index(self._bean_prefix) == 0
        except ValueError:
            pass

    def parse_bean_name(self, v):
        position = len(self._bean_prefix)
        return v[position:]