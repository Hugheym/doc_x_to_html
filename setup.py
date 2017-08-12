# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup
import os
print(os.path.curdir)
if(os.path.abspath(os.path.curdir).endswith('test')):
    package_dir = os.path.abspath('../doc_x_to_html')
    project_root = os.path.abspath('..')
else:
    package_dir = os.path.abspath('./doc_x_to_html')
    project_root = os.path.abspath('.')
READ_ME_PATH = os.path.join(project_root, "README.rst")

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open(os.path.join(package_dir, 'doc_x_to_html.py')).read(),
    re.M
).group(1)



with open(READ_ME_PATH, "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="doc_x_to_html",
    packages=['doc_x_to_html'],
    entry_points={
        "console_scripts": ['doc_x_to_html = doc_x_to_html.doc_x_to_html:main']
    },
    install_requires = ['mammoth==1.4.2']
    ,
    python_requires=">=3.0"
    ,
    version=version,
    description="Python command line application to convert multiple doc/docx files to html files.",
    long_description=long_descr,
    author="Hugh Matsubara"
)