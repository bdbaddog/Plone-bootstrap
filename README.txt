You need to run the create-plone-bootstrap.py with a python which has virtualenv and setuptools already installed.

It generates plone-try-bootstrap.py, which you can run with a python with neither virtualenv or setuptools::
 python_with_tools create-plone-bootstrap.py
 python_without_tools plone-try-boostrap.py

 New python executable in /Users/bdbaddog/devel/plone/sprint/.plone_python/bin/python
 Installing distribute.....................................................................................................................................................................................done.
 install_dir /Users/bdbaddog/devel/plone/sprint/.plone_python/lib/python2.7/site-packages/
 Searching for zc.buildout
 Reading http://pypi.python.org/simple/zc.buildout/
 Reading http://buildout.org
 Best match: zc.buildout 1.5.2
 Downloading http://pypi.python.org/packages/source/z/zc.buildout/zc.buildout-1.5.2.tar.gz#md5=87f7b3f8d13926c806242fd5f6fe36f7
 Processing zc.buildout-1.5.2.tar.gz
 Running zc.buildout-1.5.2/setup.py -q bdist_egg --dist-dir /var/folders/XG/XGgG-EP8G5i6vXYNPGLlTU+++TI/-Tmp-/easy_install-wRolnR/zc.buildout-1.5.2/egg-dist-tmp-5B_mu_
 Adding zc.buildout 1.5.2 to easy-install.pth file
 Installing buildout script to /Users/bdbaddog/devel/plone/sprint/.plone_python/bin

 Installed /Users/bdbaddog/devel/plone/sprint/.plone_python/lib/python2.7/site-packages/zc.buildout-1.5.2-py2.7.egg
 Processing dependencies for zc.buildout
 Finished processing dependencies for zc.buildout

This is a work in progress in response to this email by Alex Limi ( on behalf of Martin Aspeli)::
     
 Sending this on behalf of Martin, since he has to leave for his flight back
 to the UK:

 All,

 Problem #1 for new users on Unix platforms: Using a non-isolated system
 Python.

 We're now in a position where most Linux and Mac users will have a binary
 called python2.6 in their path, so we can have instructions like::

    $ python2.6 bootstrap.py
    $ bin/buildout

 Yay. Except if you do that with a Python you didn't compile yourself, it
 explodes in weird and wonderful ways. Compiling/installing your own Python
 is a significant barrier (I witnessed this for about 1/3rd of the people in
 my training course). And of course, this happens every time Limi tries to
 do anything Plone-related.

 A good-enough solution for most people is to use virtualenv. So now, our
 instructions become::

    $ sudo easy_install -U virtualenv
    $ virtualenv -p /usr/bin/python2.6 --no-site-packages ~/python
    $ ~/python/bin/python bootstrap.py
    $ bin/buildout

 So, here's the rub: We can do this for people in the ``bootstrap.py``.
 Right
 now, people just download the one from http://python-distribute.org, or copy
 one from another buildout. So, what if we had::

    $ python2.6 plone-bootstrap.py
    $ bin/buildout

 This would:

  * Sniff out a half-decent Python
  * Install virtualenv (ideally without needing sudo access)
  * Create a virtualenv without site packages, e.g. in a ``.python``
 directory
  * Use its isolated python to do what bootstrap does now, so
 ``bin/buildout``
    uses this

 Some key constraints/requirements

  * It has to be a single file - no package you install with setuptools
  * It has to be cross-platform (including Windows, Linux, Mac)
  * It should ideally not require a buildout.cfg in the current directory, as
    bootstrap.py does
  * It needs to print meaningful error messages if it can't figure out what
    to do in the environment
  * It may need some kind of knowledge of Plone versions to understand which
    Python versions are compatible

 Regards,
 Martin

 -- 
 Alex Limi · +limi <http://profiles.google.com/limi> · @limi · limi.net