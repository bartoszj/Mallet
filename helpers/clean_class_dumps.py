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
import sys
import imp

i = imp.find_module("lldb_additions", [".."])
imp.load_module("lldb_additions", *i)
import lldb_additions.class_dump as class_dump

# Example offsets.json file:
# {
#   "arm64": [
#     {
#       "super_class": "UIView",
#       "offset": 80
#     },
#     {
#       "class": "_UIDatePickerView",
#       "offset": 112
#     }
#   ],
#   "armv7": [
#     ...
#   ],
#   "armv7s": [
#     ...
#   ],
#   "i386": [
#     ...
#   ],
#   "x86_64": [
#     ...
#   ]
# }

def clean_class_dumps():
    # Current directory path.
    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)

    # Input / output folders.
    input_dir = os.path.join(current_dir, "ClassDumps")
    output_dir = os.path.join(current_dir, "../lldb_additions/ClassDumps")
    offsets_file_path = os.path.join(current_dir, "offsets.json")

    al = class_dump.ArchitecturesList()
    al.read_directory_path(input_dir)
    al.fix_ivars_offset(offsets_file_path)
    al.save_to_folder(output_dir)

if __name__ == "__main__":
    clean_class_dumps()
