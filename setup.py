# from distutils.core import setup
from setuptools import setup

setup(name='pydi',
    version='1.0',
    py_modules=[
        'pydi.di',
        'pydi.container',
        'pydi.exceptions',
        'pydi.functions',
        'pydi.parsers'
    ],
    install_requires=['six']
)

