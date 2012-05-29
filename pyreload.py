# (c) 20012 Jim Jose;
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
A file monitor and module reloader.

Major part of the code is taken directly from 
the original "paste.reloader" module. I just created this
stripped down version for one of my projects and wanted to
share if anyone else is interested.

**all credits goes to orginal authors @ Paste **
http://pythonpaste.org/modules/reloader.html


Use this like:
..code-block:: Python

    import pyreload
    pyreload.install(verbose=True, poll_interval=1)

- Now this will watch for any changes in the files and will reload 
the corresponding module.

"""

import os
import imp
import sys
import time
import threading

def install(verbose=True, poll_interval=1):
    """
    Install the reloading monitor.
    """
    mon = Monitor(verbose=verbose,poll_interval=poll_interval)
    t = threading.Thread(target=mon.periodic_reload)
    t.setDaemon(True)
    t.start()

class Monitor(object):
    def __init__(self, verbose, poll_interval):
        self.verbose = verbose;
        self.module_mtimes = {}
        self.poll_interval = poll_interval

    def periodic_reload(self):
        while True:
            self.check_reload()
            time.sleep(self.poll_interval)
    
    def check_reload(self):
        filenames = []
        for module in sys.modules.values():
            try:
                filename = module.__file__
            except (AttributeError, ImportError), exc:
                continue
           
            try:
                stat = os.stat(filename)
                if stat:
                    mtime = stat.st_mtime
                else:
                    mtime = 0
            except (OSError, IOError):
                continue
            
            if filename.endswith('.pyc') and os.path.exists(filename[:-1]):
                mtime = max(os.stat(filename[:-1]).st_mtime, mtime)
            elif filename.endswith('$py.class') and \
                    os.path.exists(filename[:-9] + '.py'):
                mtime = max(os.stat(filename[:-9] + '.py').st_mtime, mtime)
            if not self.module_mtimes.has_key(filename):
                self.module_mtimes[filename] = mtime
            elif self.module_mtimes[filename] < mtime:
                if self.verbose:
                    print >> sys.stderr, (
                        "pyreload: %s changed; reloading..." % filename)
                try:
                    imp.reload( module )
                    if self.verbose:
                        print >> sys.stderr, ("pyreload: reloaded: %s" % module.__name__ )
                except Exception as e:
                    if self.verbose:
                        print >> sys.stderr, ("pyreload: reloaded: %s" % e.message )
                    pass
                
                del self.module_mtimes[filename]
                            