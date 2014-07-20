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
import sys


def class_dump(j):
    d = u""
    for archName in j:
        d += u"Architecture: {}\n".format(archName)
        arch = j[archName]
        type = arch[u"type"]
        if type == u"class":
            class_name = arch["className"]
            super_class_name = arch["superClassName"]
            d += u"Class: {}\n".format(class_name)
            d += u"Super class: {}\n".format(super_class_name)
            if "ivars" in arch:
                ivars = arch["ivars"]
                # Sort ivars by offset.
                ivars = sorted(ivars, key=lambda x: x["offset"], reverse=False)
                for ivar in ivars:
                    ivarType = ivar["ivarType"]
                    name = ivar["name"]
                    size = ivar["size"]
                    offset = ivar["offset"]
                    d += u"  {0} {1} {2} (0x{2:X}) 0x{3:X}\n".format(ivarType, name, size, offset)

        d += u"\n"
    return d


if __name__ == "__main__":
    # Check number of parameters.
    if len(sys.argv) < 2:
        print "Not enough arguments"
        exit()

    # Current directory path.
    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)

    args = sys.argv[1:]
    for path in args:
        # Create absolute path.
        if not os.path.isabs(path):
            path = os.path.join(current_dir, path)

        if not os.path.exists(path):
            continue

        with open(path, "r") as f:
            json_data = json.load(f)

        dump = class_dump(json_data)
        print dump
