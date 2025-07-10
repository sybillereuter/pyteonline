from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='pyteonline',
    version='1.2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
    package_data={'pyteonline': ['templates/*.html']}
)
