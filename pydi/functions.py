from pydi.exceptions import ClassNotFoundException


def get_class(class_path):
    parts = class_path.split('.')
    module_name = ".".join(parts[:-1])
    try:
        m = __import__(module_name)
        for comp in parts[1:]:
            m = getattr(m, comp)
    except ImportError:
        raise ClassNotFoundException(class_path)

    return m
