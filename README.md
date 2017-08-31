# pydi


### Beans configuration example

    beans = {
            "test_class2": {
            "value": "class_path:app.TestClass2",
            "scope": "prototype",
        },
        "test_class": {
            "value": "class_path:app.TestClass",
            "args": ["bean:test_class2", "some value"]
        },
    }
    
### PIP install
`pip install git+https://github.com/randrienko/python-di@master`