from pydi import container

class Hello(object):
    def __init__(self, name):
        self.name = name
    
    def say(self):
        print("Hellow, {}".format(self.name))

beans = {
        "hello": {
            "value": Hello,
            "args": ["World"]
        },
        "hello2": {
            "value": "class_path:basic_di.Hello",
            "args": ["Jhon"]
        },
}

if __name__ == "__main__":
    container.setup(beans)
    
    hello = container.get("hello")
    hello.say()
    
    hello2 = container.get("hello2")
    hello2.say()