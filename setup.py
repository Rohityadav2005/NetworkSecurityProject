'''
The setup.py file is an essential part of packaging and 
distributing python projects. It is used by setuptools
(or distulits in older python versions) to define the confiquration 
of your project,such as its metadata,dependencies, and more
'''

from setuptools import find_packages,setup
from typing import List

def requirements(file_path:str)->List[str]:
    requirements_lst:List[str] = []
    try:
        with open(file_path,"r") as file_obj:
            lines = file_obj.read()

            for line in lines:
                requirement = line.strip()

                if requirement and requirement != "-e .":
                    requirements_lst.append(requirement)

    except Exception as e:
        print(" The requirement file not found")


    return requirements_lst

setup(
    name='networksecurity',
    version='0.0.0.1',
    author='Rohit Yadav',
    author_email='rohit2205x@gmail.com',
    packages=find_packages(),
    install_requires = requirements('requirements.txt') 
)    


