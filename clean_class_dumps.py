#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Bartosz Janda
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import json


def clean_ivar_json(j):
    oj = dict()

    # Standard keys.
    supported_keys = [u"alignment", u"ivarType", u"name", u"offset", u"size", u"type"]
    for key in supported_keys:
        if key in j:
            oj[key] = j[key]

    if len(oj) == 0:
        return None
    return oj


def clean_ivars_json(j):
    oj = list()

    for ivar in j:
        new_ivar = clean_ivar_json(ivar)
        if new_ivar:
            oj.append(new_ivar)

    if len(j) == 0:
        return None
    return oj


def clean_class_json(j):
    oj = dict()

    # Standard keys.
    supported_keys = [u"superClassName", u"className", u"type"]
    for key in supported_keys:
        if key in j:
            oj[key] = j[key]

    # ivars key.
    ivars_key = u"ivars"
    if ivars_key in j:
        new_ivars = clean_ivars_json(j[ivars_key])
        if new_ivars:
            oj[ivars_key] = new_ivars

    if len(oj) == 0:
        return None
    return oj


def clean_class_dump_json(j):
    oj = dict()
    for archName in j:
        arch = j[archName]
        type = arch[u"type"]
        if type == u"class":
            new_arch = clean_class_json(arch)
            if new_arch:
                oj[archName] = new_arch

    if len(oj) == 0:
        return None
    return oj


def clean_class_dumps():
    # Current directory path.
    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)

    # Input / output folders.
    input_dir = os.path.join(current_dir, "ClassDumps")
    output_dir = os.path.join(current_dir, "LLDBScripts/ClassDumps")

    # Go through all files in input directory.
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            # Check if it is a JSON file.
            if not f.endswith(".json"):
                continue

            # File path.
            fi_path = os.path.join(root, f)

            # Read JSON.
            j = None
            with open(fi_path, "r") as json_file:
                j = json.load(json_file)

            j = clean_class_dump_json(j)

            # Skip is JSON data is empty.
            if j is None:
                continue

            # Get file output directory.
            d = root.replace(input_dir, "")
            d = d.strip("/")
            d_path = os.path.join(output_dir, d)
            if not os.path.exists(d_path):
                os.makedirs(d_path)

            # Output file path.
            fo_path = os.path.join(d_path, f)

            # Save file.
            with open(fo_path, "w") as json_file:
                json.dump(j, json_file, sort_keys=True, indent=2, separators=(",", ":"))

if __name__ == "__main__":
    clean_class_dumps()
