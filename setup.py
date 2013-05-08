
import os
import sys
from distutils.core import setup


import versioneer


versioneer.versionfile_source = 'tr_connect/_version.py'
versioneer.versionfile_build = 'tr_connect/_version.py'
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = 'tr_connect-'

# setup(name='foo',
#       version='1.0',
#       py_modules=['foo'],
#       )
cmdclass = versioneer.get_cmdclass()

setup(
    name = 'tr_connect',
    version = versioneer.get_version(),
    description = 'Pythonic interface to Thomson Reuters financial databases',
    author = 'Benjamin Zaitlen',
    author_email = 'ben.zaitlen@continuum.io',
    packages = ['tr_connect'],
    package_data = {'tr_connect':['data/*']},
    cmdclass = cmdclass,
)