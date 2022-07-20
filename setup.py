from setuptools import setup, find_packages
import e4e
import os
default_requires = [
    'pandas',
    'numpy',
    'matplotlib',
    'pyserial',
    'google-api-python-client',
    'google-auth-httplib2',
    'google-auth-oauthlib',
    'ipython',
    'pyyaml',
]
pi_requires = [
    'gpiozero',
    'RPi.GPIO'
]

if os.path.exists('/sys/firmware/devicetree/base/model'):
    with open('/sys/firmware/devicetree/base/model', 'r') as model:
        pi_name = model.read()
        if pi_name.find('Raspberry Pi') != -1:
            default_requires.extend(pi_requires)
setup(
    name='SmartfinFWTest',
    version=e4e.__VERSION__,
    author='UCSD Engineers for Exploration',
    author_email='e4e@eng.ucsd.edu',
    install_requires=default_requires,
    packages=find_packages()
)