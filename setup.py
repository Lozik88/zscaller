from setuptools import setup
reqs = open('requirements.txt').read().split('\n')
setup(
    name="zscaller",
    version="1.0",
    packages=['zscaller'],
    install_requires=reqs
)
