from setuptools import setup, find_packages

setup(
    name='gspc',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'numba',
        'scipy'
    ],
    author='Julien Perradin',
    author_email='julien.perradin@umontpellier.fr',
    description='GSPC package is a package for computing structural properties of glasses',
    url='https://github.com/JulienPerradin/gspc',
)