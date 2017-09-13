from setuptools import setup
# For converting markdown README to rst: pandoc --from=markdown --to=rst README.md -o README.rst
setup(name='botty_mcbotface',
      version='0.1',
      description='General purpose Slack-bot with personality',
      url='https://github.com/ColumbiaSC-Tech/botty_mcbotface',
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
