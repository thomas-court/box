from setuptools import setup, find_packages

with open("requirements.txt") as f:
  required = f.read().splitlines()

setup(
  name = 'genbox',
  version = '0.1.0',
  install_requires = required,
  packages = find_packages(),
  include_package_data = True,
  entry_points = {
   'console_scripts': ['box = genbox.main:main']  
 }

)
