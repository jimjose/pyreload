pyreload
========

File monitor and module reloader for Python apps.

Major part of the code is taken directly from the original "paste.reloader" module. I just created this stripped down version for one of my projects and wanted to share if anyone else is interested.

**all credits goes to original authors @ Paste **
http://pythonpaste.org/modules/reloader.html

Use this like:
..code-block:: Python

    import pyreload
    pyreload.install(verbose=True, poll_interval=1) # both optional

Now this will watch for any changes in the files and will reload the corresponding module automatically, so there is no need to restart the python server.
