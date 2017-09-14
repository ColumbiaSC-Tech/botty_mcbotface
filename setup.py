#!/usr/bin/env python
from setuptools import setup

setup(name='botty_mcbotface',
      version='1.0',
      description='General purpose Slack-bot with personality',
      url='https://github.com/ColumbiaSC-Tech/botty_mcbotface',
      author='Danny Hinshaw',
      author_email='danny@nulleffort.com',
      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      install_requires=[
          'bs4',
          'lxml',
          'requests',
          'slackbot'
      ],
      keywords='slack bot slackbot',
      license='MIT',
      packages=['botty_mcbotface'],
      package_data={
          '': ['*.json', '*.rst', '*.txt'],
      },
      python_requires='>=3',
      zip_safe=False)
