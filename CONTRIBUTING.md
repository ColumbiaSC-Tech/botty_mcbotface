# botty_mcbotface developer guide

Thanks for your interest in developing botty_mcbotface! These notes should help you produce pull
requests that will get merged without any issues.

## Style guide

### Code style

There are places in the code that do not follow PEP 8 conventions. Do follow PEP 8 with new code,
but do not fix formatting throughout the file you're editing. If your commit has a lot of unrelated
reformatting in addition to your new/changed code, you may be asked to resubmit it with the extra changes removed.

### Commits

It's a good idea to use one branch per pull request. This will allow you to work on multiple changes at once.

Most pull requests should contain only a single commit. If you have to make corrections to a pull
request, rebase and squash your branch, then do a forced push. Clean up the commit message so it's
clear and as concise as needed.

## Developing

These steps will help you prepare your development environment to work on botty_mcbotface.

### Clone the repo

Begin by forking the repo. You will then clone your fork and add the central repo as another remote.
This will help you incorporate changes as you develop.

```
$ git clone git@github.com:yourusername/botty_mcbotface.git
$ cd botty_mcbotface
$ git remote add upstream git@github.com:lins05/botty_mcbotface.git
```

Do not make commits to develop, even in your local copy. All commits should be on a branch. Start your branch:

```
$ git checkout develop -b name_of_feature
```

To incorporate upstream changes into your local copy and fork:

```
$ git checkout develop
$ git fetch upstream
$ git merge upstream/master
$ git push origin develop
```


See git documentation for info on merging, rebasing, and squashing commits.

### virtualenv/pyvenv

A virtualenv allows you to install the Python packages you need to develop and run botty_mcbotface without
adding a bunch of unneeded junk to your system's Python installation. Once you create the virtualenv,
you need to activate it any time you're developing or running botty_mcbotface.
For Python 3, run:

```
$ pyvenv .env
```

Now that the virtualenv has been created, activate it and install the packages needed for development:

```
$ source .env/bin/activate
$ pip install -r requirements.txt
```

At this point, you should be able to run botty_mcbotface as described in the README.
