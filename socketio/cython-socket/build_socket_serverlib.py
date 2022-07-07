from setuptools import setup
from Cython.Build import cythonize

setup(
    name='libclient',
    ext_modules=cythonize("libserver.pyx"),
    zip_safe=False,
)

