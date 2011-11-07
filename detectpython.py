#
# application boot script

import os
import sys

try:
    version_info = sys.version_info
except AttributeError:
    version_info = 1, 5 # 1.5 or older

REINVOKE = "__MYAPP_REINVOKE"
NEED_VERS = (2, 6)
KNOWN_PYTHONS = ('python2.5',)

if version_info < NEED_VERS:
if not os.environ.has_key(REINVOKE):
    # mutating os.environ doesn't work in old Pythons
    os.putenv(REINVOKE, "1")
    for python in KNOWN_PYTHONS:
        try:
            os.execvp(python, [python] + sys.argv)
        except OSError:
            pass
            print >>sys.stderr, "error: cannot find a suitable python interpreter"
            print >>sys.stderr, " (need %d.%d or later)" % NEED_VERS
            sys.exit(1)

if hasattr(os, "unsetenv"):
    os.unsetenv(REINVOKE)

#
# get things going!

import myapp
myapp.run()

# end of boot script