# only used for testing... pip install -e .
from setuptools import setup, find_packages

setup(name="since", packages=find_packages('src'), package_dir={'': 'src'})
