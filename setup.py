from setuptools import setup
#test
#another test
setup(name='pyrasplcd',
      version='0.3',
      description='Have your embedded machine print how it feels.',
      url='https://github.com/jmtyson/pyrasplcd',
      author='Jeffrey M Tyson',
      author_email='jeff.tyson@gmail.com',
      license='MIT',
      packages=['pyrasplcd'],
      install_requires=['pyserial','PIL'],
      zip_safe=False)