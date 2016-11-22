from setuptools import setup
import sys

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')

setup(name='prawbot',
      version='0.1',
      description='A minimal framework for creating Reddit Bots using PRAW',
      url='https://github.com/JKolios/prawbot',
      author='JKolios',
      author_email='jason.kolios@gmail.com',
      license='MIT',
      packages=['funniest'],
      install_requires=[
          'praw>=3.6.0',
          'Flask>=0.11.1'
      ],
      zip_safe=False,
      keywords='reddit bot praw')
