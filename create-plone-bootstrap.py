import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess

def adjust_options(options, args):
    # Create virtualenv in current dir
    args.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.plone_python'))

    options.no_site_packages = True
    options.verbose = 1


def after_install(options, home_dir):
    etc = join(home_dir, 'etc')
    if not os.path.exists(etc):
        os.makedirs(etc)
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                     'zc.buildout'])
"""))
f = open('plone-try-bootstrap.py', 'w').write(output)
