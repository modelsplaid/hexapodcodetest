from setuptools import setup
from Cython.Build import cythonize

setup(
    name='libclient',
    ext_modules=cythonize("libclient.pyx"),
    zip_safe=False,
)

