from pydi import container


class Observable(object):
    p1 = None

    def __init__(self):
        self.observers = []

    def notify(self, data):
        for observer in self.observers:
            observer.process(data)


class Observer1(object):

    def process(self, data):
        print("{}. \n Data: {}".format(self.__class__, data))


class Observer2(object):

    def process(self, data):
        print("{}. \n Data: {}".format(self.__class__, data))


beans = {
    "observable": {
        "value": "class_path:observer_di.Observable",
        "properties": {
            "observers": ["bean:observer1", "bean:observer2"]
        }
    },
    "observer1": {
        "value": "class_path:observer_di.Observer1",
    },
    "observer2": {
        "value": "class_path:observer_di.Observer2",
    }
}

if __name__ == "__main__":
    container.setup(beans)

    o = container.get("observable")
    o.notify("Hello")



