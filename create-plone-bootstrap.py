import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess

def adjust_options(options, args):
    # Create virtualenv in current dir
    #args.append(os.path.dirname(os.path.abspath(__file__)))
    args.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.plone_python'))

    options.no_site_packages = True
    options.verbose = 2


def after_install(options, home_dir):

##    subprocess.call([join(home_dir, 'bin', 'easy_install'),
###                     '-s','bin',
##                     'zc.buildout'])

    import sys
    if sys.platform == 'win32':
        def quote(c):
            if ' ' in c:
                return '"%s"' % c # work around spawn lamosity on windows
            else:
                return c
    else:
        def quote (c):
            return c


    import tempfile
    tmpeggs = tempfile.mkdtemp()
    VERSION = ''

    if options.use_distribute:
        requirement = 'distribute'
    else:
        requirement = 'setuptools'

    try:
        import pkg_resources
        import setuptools
        if not hasattr(pkg_resources, '_distribute'):
            raise ImportError
    except ImportError:
        import urllib2
        ez = {}
        if options.use_distribute:
            exec urllib2.urlopen('http://python-distribute.org/distribute_setup.py'
                                 ).read() in ez
            ez['use_setuptools'](to_dir=tmpeggs, download_delay=0, no_fake=True)
        else:
            exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py'
                                 ).read() in ez
            ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)

        reload(sys.modules['pkg_resources'])
        import pkg_resources



    ws  = pkg_resources.working_set
    cmd = 'from setuptools.command.easy_install import main; main()'
    assert os.spawnle(
        os.P_WAIT, sys.executable, quote (sys.executable),
        '-c', quote (cmd), '-mqNxd', quote (tmpeggs), 'zc.buildout' + VERSION,
        dict(os.environ,
            PYTHONPATH=
            ws.find(pkg_resources.Requirement.parse(requirement)).location
            ),
        ) == 0

    
    ws.add_entry(tmpeggs)
    ws.require('zc.buildout' + VERSION)
    import zc.buildout.buildout
    args=[]
    zc.buildout.buildout.main(args)

"""))
f = open('plone-try-bootstrap.py', 'w').write(output)
