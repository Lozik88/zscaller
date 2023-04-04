from setuptools import setup
import os
reqs = open(os.path.join('zscaller','requirements.txt')).read().split('\n')
setup(
    name="zscaller",
    version="1.0",
    packages=['zscaller'],
    install_requires=reqs
)
