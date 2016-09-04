#!/usr/bin/env python

VERSION = '0.0.2'

import glob
from setuptools import setup
setup(
    name = "hocr-spec",
    version = VERSION,
    packages = ['hocr_spec'],
    description = 'Implementation of the hOCR specs',
    author = 'Konstantin Baierer',
    author_email = 'konstantin.baierer@gmail.com',
    url = 'https://github.com/kba/hocr-spec-python',
    download_url = 'https://github.com/kba/hocr-spec-python/tarball/v' + VERSION,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Utilities',
    ],
    install_requires = [
        'lxml',
    ],
    scripts = ['hocr-spec']
)
