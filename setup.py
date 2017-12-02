#!/usr/bin/env python

from setuptools import setup


def readme():
    """Grab the rst version of docs for pypi."""
    with open('README.rst') as f:
        return f.read()


setup(name='botty_mcbotface',
      version='1.3.8',
      description='General purpose Slack-bot with personality',
      long_description=readme(),
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
          'apscheduler',
          'arrow',
          'bs4',
          'cchardet',
          'lxml',
          'nose',
          'pytz',
          'requests',
          'slackbot',
          'sqlalchemy'
      ],
      keywords='slack bot slackbot botty_mcbotface botty gonzobot',
      license='MIT',
      packages=['botty_mcbotface',
                'botty_mcbotface.botty',
                'botty_mcbotface.botty.db',
                'botty_mcbotface.botty.db.models',
                'botty_mcbotface.botty.db.routines',
                'botty_mcbotface.data',
                'botty_mcbotface.plugins',
                'botty_mcbotface.utils'],
      package_data={
          '': ['*.json', '*.rst', '*.txt'],
      },
      python_requires='>=3.5',
      zip_safe=False)
