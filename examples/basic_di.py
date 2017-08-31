from pydi import container

class Hello(object):
    p1 = None
    
    def __init__(self, name):
        self.name = name
    
    def say(self):
        print("Hellow, {}".format(self.name))


class Hello2(object):
    def __init__(self, hello_obj):
        self._hello_obj = hello_obj
        self.some_property

    def say(self):
        print("hellow2 say:")
        self._hello_obj.say()
        print(self.some_property)

beans = {
    "hello": {
        "value": "class_path:basic_di.Hello",
        "args": ["Worldwewew"],
        "properties": {
            "p1": "property value"
        }
    },
    "hello2": {
        "value":"class_path:basic_di.Hello2",
        "args": ["bean:hello"],
        "properties": {
            "some_property": 100
        }

    },
}

if __name__ == "__main__":
    container.setup(beans)
    
    hello = container.get("hello")
    print(hello)
    hello.say()

    hello2 = container.get("hello2")
    hello2.say()
    print(hello2.some_property)
