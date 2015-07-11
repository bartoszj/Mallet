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
import imp
import argparse
import tabulate

i = imp.find_module("lldb_additions", [".."])
imp.load_module("lldb_additions", *i)
import lldb_additions.class_dump as class_dump


_whitespace = u"\u200b"


def normalize_type(type_32bit, type_64bit):
    if type_32bit is None:
        type_32bit = type_64bit
    elif type_64bit is None:
        type_64bit = type_32bit

    if type_32bit == type_64bit:
        if type_32bit == u"struct CGPoint":
            return u"CGPoint"
        elif type_32bit == u"struct CGSize":
            return u"CGSize"
        elif type_32bit == u"struct CGRect":
            return u"CGRect"
        elif type_32bit == u"struct UIEdgeInsets":
            return u"UIEdgeInsets"
        elif type_32bit == u"struct __CFDictionary *":
            return u"NSDictionary *"
        elif type_32bit == u"struct _NSRange":
            return u"NSRange"
        return type_32bit
    elif type_32bit == u"BOOL" and type_64bit == u"bool":
        return u"BOOL"
    elif type_32bit == u"char" and type_64bit == u"_Bool":
        return u"BOOL"
    elif type_32bit == u"int" and type_64bit == u"long long":
        return u"NSInteger"
    elif type_32bit == u"long" and type_64bit == u"long long":
        return u"NSInteger"
    elif type_32bit == u"unsigned int" and type_64bit == u"unsigned long long":
        return u"NSUInteger"
    elif type_32bit == u"unsigned long" and type_64bit == u"unsigned long long":
        return u"NSUInteger"
    elif type_32bit == u"float" and type_64bit == u"double":
        return u"CGFloat"
    elif type_32bit == u"struct CADoublePoint" and type_64bit == u"struct CGPoint":
        return u"CADoublePoint"

    print("Different types: {} != {}".format(type_32bit, type_64bit))
    return type_64bit


def dump_class(module_name, class_name):
    """
    Prints class description.

    :param str module_name: Module name.
    :param str class_name: Class name.
    """
    # Current directory path.
    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)
    input_dir = os.path.join(current_dir, u"../lldb_additions/summaries/{}/{}".format(module_name, class_dump.class_dumps_folder_name))
    input_dir = os.path.normpath(input_dir)

    m = class_dump.Module(module_name, input_dir)
    architectures = [u"armv7", u"i386", u"arm64", u"x86_64"]
    main_architecture = u"arm64"
    architecture_32bit = u"armv7"
    architecture_64bit = u"arm64"
    classes = [m.get_class_or_load(a, class_name) for a in architectures]
    main_class = m.get_class_or_load(main_architecture, class_name)

    # Output.
    output = u"Class: {}\n".format(class_name)
    if main_class.super_class_name:
        output += u"Super class: {}\n".format(main_class.super_class_name)
    if main_class.protocols:
        output += u"Protocols: {}\n".format(u", ".join(main_class.protocols))

    # iVars.
    ivars = sorted(main_class.ivars, key=lambda x: x.offset, reverse=True)
    if ivars:
        # Headers
        headers = [u"Name"]
        [headers.append(a) for a in architectures]

        rows = list()
        for ivar in ivars:
            # iVars for all architectures.
            architecture_ivars = [cl.get_ivar(ivar.name) for cl in classes]
            architecture_ivar_32bit = architecture_ivars[architectures.index(architecture_32bit)]
            architecture_ivar_64bit = architecture_ivars[architectures.index(architecture_64bit)]

            # Normalized type name.
            type32 = architecture_ivar_32bit.ivarType if architecture_ivar_32bit else None
            type64 = architecture_ivar_64bit.ivarType if architecture_ivar_64bit else None
            type_name = normalize_type(type32, type64)
            splitted_type_name = type_name.split(u"\n")

            # For multiline types add "empty" rows.
            ivar_rows = list()
            for type_line in splitted_type_name[:-1]:
                type_row = [type_line.replace(u" ", _whitespace)] + [u""] * len(architectures)
                ivar_rows.append(type_row)

            # Add type line.
            type_row = [u"{} {}".format(splitted_type_name[-1], ivar.name).replace(u" ", _whitespace)]
            for architecture_ivar in architecture_ivars:
                value = u"{0:>3} 0x{0:03X} / {1:<2}".format(architecture_ivar.offset if architecture_ivar is not None else -1,
                                                            architecture_ivar.size if architecture_ivar is not None else None).replace(u" ", _whitespace)
                type_row.append(value)

            ivar_rows.append(type_row)
            ivar_rows.reverse()  # Ivars are reversed, so rows for ivar also have to be reversed.
            rows.extend(ivar_rows)

        rows.reverse()
        output += tabulate.tabulate(rows, headers)

    print(output)


if __name__ == "__main__":
    # Argument parser.
    parser = argparse.ArgumentParser(description="Prints class description.")
    parser.add_argument("-m", "--module", required=True)
    parser.add_argument("class")

    # Parse arguments.
    args = parser.parse_args()
    class_name = vars(args)["class"]
    module_name = args.module

    dump_class(module_name, class_name)
