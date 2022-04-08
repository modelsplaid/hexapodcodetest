from setuptools import setup
from Cython.Build import cythonize

setup(
    name='lib client lib',
    ext_modules=cythonize("libclient.pyx"),
    zip_safe=False,
)                                                                                                                    
