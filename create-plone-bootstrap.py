import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess, sys, tempfile, urllib2

args_holder = None

def extend_parser(parser):
    parser.add_option("-b", "--buildout_version", dest="buildout_version",
                      default='1.4.4',
                      help="use a specific zc.buildout version")

    parser.add_option("-c", None, action="store", dest="config_file",
                       help=("Specify the path to the buildout configuration "
                             "file to be used."))

def adjust_options(options, args):
    req_python=(2,6)
    if sys.version_info <= req_python:
        print('ERROR: Plone requires Python %d.%d or greater.'%req_python )
        sys.exit(101)
        
    # Create virtualenv in current dir
    #args.append(os.path.dirname(os.path.abspath(__file__)))
    args.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.python'))

    options.no_site_packages = True
#    options.verbose = 2

    args_holder = list(args)

    # Hack..
    # If we're already in a virtualenv, don't create a new one
    virtualenv_dir = os.environ.get('VIRTUAL_ENV',False)
    if virtualenv_dir:
        print "Info: You're already in an virtualenv %s so we won't create a new one"%virtualenv_dir
        old_plone_bootstrap(options,args[0])
        sys.exit(0)


def after_install(options, home_dir):
##    # Install buildout using our virtualenv'd
##    easy_install = join(home_dir, 'bin', 'easy_install')
##    print "ei: %s"%easy_install
##    subprocess.call([easy_install,
##                     '-s','bin',
##                     'zc.buildout==%s'%options.buildout_version ])

##    import pkg_resources
##    import setuptools

##    ws  = pkg_resources.working_set
##    ws.require('zc.buildout==%s'%options.buildout_version)
##    import zc.buildout.buildout
##    zc.buildout.buildout.main(args)
    old_plone_bootstrap(options,home_dir)


def old_plone_bootstrap(options,home_dir):

    args = args_holder
    print "ARGS:%s"%args_holder
    if not args:
        args = []
    tmpeggs = tempfile.mkdtemp()

    # if -c was provided, we push it back into args for buildout' main function
    if options.config_file is not None:
        args += ['-c', options.config_file]

    args = args + ['bootstrap']

    try:
        import pkg_resources
        import setuptools
        if not hasattr(pkg_resources, '_distribute'):
            raise ImportError
    except ImportError:
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

    if sys.platform == 'win32':
        def quote(c):
            if ' ' in c:
                return '"%s"' % c # work around spawn lamosity on windows
            else:
                return c
    else:
        def quote (c):
            return c

    cmd = 'from setuptools.command.easy_install import main; main()'
    ws  = pkg_resources.working_set

    if options.use_distribute:
        requirement = 'distribute'
    else:
        requirement = 'setuptools'

    assert os.spawnle(
        os.P_WAIT, sys.executable, quote (sys.executable),
        '-c', quote (cmd), '-mqNxd', quote (tmpeggs), 'zc.buildout==%s'%options.buildout_version,
        dict(os.environ,
             PYTHONPATH=
             ws.find(pkg_resources.Requirement.parse(requirement)).location
             ),
        ) == 0

    ws.add_entry(tmpeggs)
    ws.require('zc.buildout==%s'%options.buildout_version)
    import zc.buildout.buildout
    zc.buildout.buildout.main(args)
    shutil.rmtree(tmpeggs)


"""))
f = open('plone-try-bootstrap.py', 'w').write(output)
