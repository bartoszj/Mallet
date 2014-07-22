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
import ClassDump


def dump_class(class_name):
    # Current directory path.
    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)
    input_dir = os.path.join(current_dir, "LLDBScripts/ClassDumps")

    al = ClassDump.ArchitecturesList()
    al.read_directory_path(input_dir)
    all_classes = al.all_class_names()
    if class_name in all_classes:
        output = u""
        for architecture in al.architectures:
            c = architecture.get_class(class_name)
            output += u"Architecture: {}\n".format(architecture.name)
            output += u"Class: {}\n".format(c.class_name)
            output += u"Super class: {}\n".format(c.super_class_name)
            output += u"Protocols: {}\n".format(u", ".join(c.protocols))
            output += u"Ivars:\n"
            ivars = sorted(c.ivars, key=lambda x: x.offset, reverse=False)
            for ivar in ivars:
                output += u"  {0} {1} {2} (0x{2:X}) 0x{3:X}\n".format(ivar.ivarType, ivar.name, ivar.size, ivar.offset)
            output += u"\n"
        print output


if __name__ == "__main__":
    # Check number of parameters.
    if len(sys.argv) != 2:
        print "Wrong number of parameters"
        exit()

    dump_class(sys.argv[1])
