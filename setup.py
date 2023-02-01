#!/usr/bin/env python3
import os
import re
import glob
from setuptools import setup, find_packages


__dir__ = os.path.dirname(__file__)

version_rx = re.compile(r"__version__ = \"([^\"]+)\"\n")
version_file_str = open(os.path.join("openlane", "__version__.py")).read()
version = version_rx.match(version_file_str)[1]

requirements = open("requirements.txt").read().strip().split("\n")
setup(
    name="openlane",
    packages=find_packages(),
    package_data={
        "openlane": [
            "py.typed",
            "scripts/*",
            "scripts/**/*",
            "scripts/**/**/*",
        ]
    },
    version=version,
    description="A full open source RTL to GDSII flow",
    long_description=open("Readme.md").read(),
    long_description_content_type="text/markdown",
    author="Efabless Corporation and Contributors",
    author_email="donn@efabless.com",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    entry_points={"console_scripts": ["openlane = openlane.__main__:cli"]},
    python_requires=">3.8",
)
