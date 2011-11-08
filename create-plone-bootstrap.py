import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess


def extend_parser(parser):
    parser.add_option("-b", "--buildout_version", dest="buildout_version",
                      default='1.4.4',
                      help="use a specific zc.buildout version")


def adjust_options(options, args):
    # Create virtualenv in current dir
    #args.append(os.path.dirname(os.path.abspath(__file__)))
    args.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.python'))

    options.no_site_packages = True
#    options.verbose = 2


def after_install(options, home_dir):
    # Install buildout using our virtualenv'd
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                     '-s','bin',
                     'zc.buildout==%s'%options.buildout_version ])

"""))
f = open('plone-try-bootstrap.py', 'w').write(output)
