from setuptools import setup, find_packages

setup(
    name='gspc',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/JulienPerradin/gspc',
    license='<Your-License>',
    author='Julien Perradin',
    author_email='julien.perradin@umontpellier.fr',
    description='This module is a tool to analyze the structural properties of glasses from molecular dynamics simulations.',
    install_requires=[
        # Add your project dependencies here
        'numpy >= 1.26.4',
        'numba >= 0.54.1',
        'tqdm >= 4.62.3',
        'datetime >= 4.3',
        'scipy >= 1.7.3',
        'setuptools >= 58.2.0',
    ],
    classifiers=[
        # Add classifiers that match your project
        # Check https://pypi.org/classifiers/ for the full list
    ],
    python_requires='>=3.9.18',
)