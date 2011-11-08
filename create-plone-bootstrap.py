import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess

def adjust_options(options, args):
    # Create virtualenv in current dir
    #args.append(os.path.dirname(os.path.abspath(__file__)))
    args.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.plone_python'))

    options.no_site_packages = True
#    options.verbose = 2


def after_install(options, home_dir):

    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                     '-s','bin',
                     'zc.buildout==1.4.4'])

    import tempfile,urllib2
    tmpeggs = tempfile.mkdtemp()

    tarFileName=os.path.join(tmpeggs,'Imaging-1.1.7.tar.gz')
    open(tarFileName,'w').write(urllib2.urlopen('http://effbot.org/downloads/Imaging-1.1.7.tar.gz').read())
    import tarfile
    tf=tarfile.open(tarFileName,'r')
    tf.extractall(path=tmpeggs)
             
    subprocess.call([join(home_dir, 'bin', 'python'),
                     
                     os.path.join(tmpeggs,'Imaging-1.1.7','setup.py'),
                     'install'])


#    subprocess.call([join(home_dir, 'bin', 'easy_install'),
#                     'PIL'])


"""))
f = open('plone-try-bootstrap.py', 'w').write(output)
