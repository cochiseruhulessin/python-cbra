#!/usr/bin/env python3
#
# Copyright (C) 2019-2020 Cochise Ruhulessin
#
# This file is part of cbra.
#
# cbra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# cbra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cbra.  If not, see <https://www.gnu.org/licenses/>.
import json
import os
import sys
from setuptools import find_namespace_packages
from setuptools import setup

curdir = os.path.abspath(os.path.dirname(__file__))
version = str.strip(open('VERSION').read())
opts = json.loads((open('cbra/package.json').read()))
if os.path.exists('requirements.txt'):
    opts['install_requires'] = [x for x in
        str.splitlines(open('requirements.txt').read()) if x]

if os.path.exists(os.path.join(curdir, 'README.md')):
    with open(os.path.join(curdir, 'README.md'), encoding='utf-8') as f:
        opts['long_description'] = f.read()
        opts['long_description_content_type'] = "text/markdown"

setup(
    name='cbra',
    version=version,
    packages=find_namespace_packages(),
    include_package_data=True,
    **opts)
