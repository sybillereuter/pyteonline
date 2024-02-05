from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='pyteonline',
    version='1.0.3',
    packages=find_packages('pyteonline', exclude='*test*'),
    install_requires=install_requires,
    include_package_data=True,
    package_data={
        'pyteonline': ['templates/*.html']
    }
)
