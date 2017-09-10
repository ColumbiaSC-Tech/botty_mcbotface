from setuptools import setup

setup(name='botty_mcbotface',
      version='0.1',
      description='General purpose Slack-bot with personality',
      url='tbd',
      author='Danny Hinshaw',
      author_email='danny@nulleffort.com',
      install_requires=[
          'bs4',
          'lxml',
          'requests',
          'slackbot'
      ],
      license='MIT',
      packages=['botty_mcbotface'],
      zip_safe=False)
