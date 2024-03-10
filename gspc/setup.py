from setuptools import setup, find_packages

setup(
    name='gspc',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'your_script_name = your_package_name.module_name:main'
        ]
    },
    install_requires=[
        # Add your dependencies here
    ],
    author='Julien Perradin',
    author_email='julien.perradin@umontpellier.fr',
    description='GSPC is a python package for the structural properties of glasses.',
    url='https://github.com/JulienPerradin/gspc',
)