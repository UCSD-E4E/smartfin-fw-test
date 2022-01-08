from setuptools import setup, find_packages
import e4e

setup(
    name='SmartfinFWTest',
    version=e4e.__VERSION__,
    author='UCSD Engineers for Exploration',
    author_email='e4e@eng.ucsd.edu',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'gpiozero',
        'pyserial',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'ipython',
        'pyyaml',
        'RPi.GPIO'
    ],
    packages=find_packages()
)