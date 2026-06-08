from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return List of requirements
    
    '''
    requireement_lst:List[str] = []
    try:
        with open('requirements.txt','r') as f:
            #Readlines from the file
            lines =f.readlines()
            for line in lines:
                requirement = line.strip()
                #Ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requireement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")

    return requireement_lst

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author = "Rohan Pal",
    author_email = "pal.rohan0408@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)
