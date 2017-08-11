class BeanNotExistException(Exception):
    def __init__(self, bean_name):
        message = "Bean `{}` not in container.".format(bean_name)
        super(BeanNotExistException, self).__init__(message)
        
class ClassNotFoundException(Exception):
    def __init__(self, class_path):
        message = "Class `{}` not found.".format(class_path)
        super(ClassNotFoundException, self).__init__(message)
