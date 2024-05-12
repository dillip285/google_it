from setuptools import setup, find_packages

setup(
    name='google_it',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
        'beautifulsoup4',
        'requests',
        # Add other dependencies if needed
    ],
    author='nomad',
    author_email='dillip285',
    description='A Python library to perform various Google searches and extract information.',
    url='https://github.com/dillip285/google_it',
)
