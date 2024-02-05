from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='pyteonline',
    version='1.0.1',
    packages=['pyteonline'],
    install_requires=install_requires,
    package_data={'pyteonline': ['*']}
)
