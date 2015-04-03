#!/usr/bin/python


##################################
#
#   pyGEarth setup file
#
#   By: Eric Powell
#
#   Date: 11/11/2007
##################################


from distutils.core import setup
setup (name='pyGEarth',
       version='0.1.2',
       description='Set of classes to provide KML import/export functionality',
       author='Eric Powell',
       author_email='ebpowell@atlanticbb.net',
       url='http://sourceforge.net/projects/pygearth',
       download_url='http://sourceforge.net/project/showfiles.php?group_id=205211',
       packages=['pyGEarth'],
       package_dir = {'pyGEarth': 'pyGEarth'},
       classifiers=['Development Status :: 1 - Pre-Alpha',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'License :: GPLV3',
                    'Programming Language :: Python',
                    'Topic :: GIS Utilities :: Data Manipulation',
                    'Topic :: Software Develoment'],
       data_files=[('lib\site-packages\pyGEarth',['README.txt']), ('lib\site-packages', ['pyGEarth.pth'])])
