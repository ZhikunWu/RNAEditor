"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""
import sys, os
from setuptools import setup

#root = '/dist/RnaEditor.app/Contents'
#pythonhome = os.path.join(root, 'Frameworks/Python.framework/Versions/Current')

APP = ['Main.py']
DATA_FILES = ['ui/icons/rnaEditor_icon.pdf','ui/icons/rnaEditor_icon.png','ui/icons/rnaEditor_icon.svg','configuration.txt']
OPTIONS = {'argv_emulation': True,
'iconfile': '/Users/david/git/rnaEditor/ui/icons/rnaEditor.icns',
'plist': {'CFBundleShortVersionString':'0.1.0'}
}

setup(
    app=APP,
    name='RnaEditor',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)