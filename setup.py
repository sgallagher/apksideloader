#!/usr/bin/python3

import glob

from setuptools import setup

setup(
    name='apksideloader',
    version='0.1',
    packages= ['apksideloader'],
    data_files=[
        ('share/applications', ['data/com.gallagherhome.apksideloader.desktop']),
        ('share/icons/hicolor/192x192', glob.glob('data/icons/hicolor/192x192/*'))
    ],
    entry_points={
        'console_scripts': [
            'apksideloader=apksideloader.cli:main'],
    },
)
