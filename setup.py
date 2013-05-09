
import os
import sys
from distutils.core import setup


import versioneer


versioneer.versionfile_source = 'TR_CONNECT/tr_connect/_version.py'
versioneer.versionfile_build = 'tr_connect/_version.py'
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = 'tr_connect-'

cmdclass = versioneer.get_cmdclass()

setup(
    name = 'tr_connect',
    version = versioneer.get_version(),
    description = 'Pythonic interface to Thomson Reuters financial databases',
    author = 'Benjamin Zaitlen',
    author_email = 'ben.zaitlen@continuum.io',
    packages = ['tr_connect'],
    package_dir = {'tr_connect':''},
    include_package_data=True,
    package_data = {'tr_connect':['data/*','examples/*']},
    install_requires=['iopro>=1.4.3', 'pandas>=0.10.1','numpy>=1.7'],
    cmdclass = cmdclass,
)