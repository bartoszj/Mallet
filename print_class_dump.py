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
import lldb_additions.scripts.class_dump as class_dump


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
    elif type_32bit == u"unsigned int" and type_64bit == u"unsigned long long":
        return u"NSUInteger"
    elif type_32bit == u"float" and type_64bit == u"double":
        return u"CGFloat"
    elif type_32bit == u"struct CADoublePoint" and type_64bit == u"struct CGPoint":
        return u"CADoublePoint"

    print("Different types: {} != {}".format(type_32bit, type_64bit))
    return type_64bit


def dump_class(class_name):
    # Current directory path.
    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)
    input_dir = os.path.join(current_dir, "lldb_additions/ClassDumps")

    al = class_dump.ArchitecturesList()
    al.read_directory_path(input_dir)

    architecture_armv7 = al.get_architecture("armv7")
    architecture_i386 = al.get_architecture("i386")
    architecture_arm64 = al.get_architecture("arm64")
    architecture_x86_64 = al.get_architecture("x86_64")

    all_classes = al.all_class_names()
    if class_name in all_classes:
        # Classes for all architectures.
        cl_armv7 = architecture_armv7.get_class(class_name)
        cl_arm64 = architecture_arm64.get_class(class_name)
        cl_i386 = architecture_i386.get_class(class_name)
        cl_x86_64 = architecture_x86_64.get_class(class_name)
        cl = cl_arm64

        output = u""
        # Class name.
        output += u"Class: {}\n".format(cl.class_name)
        # Super class name.
        if cl.super_class_name:
            output += u"Super class: {}\n".format(cl.super_class_name)
        # Protocol names.
        if cl.protocols:
            output += u"Protocols: {}\n".format(u", ".join(cl.protocols))
        # iVars.
        ivars = sorted(cl.ivars, key=lambda x: x.offset, reverse=False)

        if ivars:
            # Find longest type name nad ivar name.
            longest_type_length = 0
            longest_ivar_length = 0
            longest_type_and_ivar_length = 0
            for ivar in ivars:
                ivar_armv7 = cl_armv7.get_ivar(ivar.name)
                ivar_arm64 = cl_arm64.get_ivar(ivar.name)
                ivar_i386 = cl_i386.get_ivar(ivar.name)
                ivar_x86_64 = cl_x86_64.get_ivar(ivar.name)

                type32 = ivar_armv7.ivarType if ivar_armv7 else None
                type64 = ivar_arm64.ivarType if ivar_arm64 else None

                type_name = normalize_type(type32, type64)
                max_type_length = max(len(nt) for nt in type_name.split(u"\n"))
                last_type_length = len(type_name.split(u"\n")[-1])

                longest_type_length = max(longest_type_length, max_type_length)
                longest_ivar_length = max(longest_ivar_length, len(ivar.name))
                longest_type_and_ivar_length = max(longest_type_and_ivar_length,
                                                   max_type_length,
                                                   last_type_length+len(ivar.name)+1)

            offset_width = 21
            output += u"{Name:{name_width}} {ArmV7:{o_width}} {i386:{o_width}} {Arm64:{o_width}} {x86_64:{o_width}}\n"\
                .format(Name=u"Name:",
                        ArmV7=u"    armv7", i386=u"    i386", Arm64=u"    arm64", x86_64=u"    x86_64",
                        name_width=longest_type_and_ivar_length, o_width=offset_width)

            for ivar in ivars:
                # Ivars.
                ivar_armv7 = cl_armv7.get_ivar(ivar.name)
                ivar_arm64 = cl_arm64.get_ivar(ivar.name)
                ivar_i386 = cl_i386.get_ivar(ivar.name)
                ivar_x86_64 = cl_x86_64.get_ivar(ivar.name)

                # Next ivars.
                index = ivars.index(ivar) + 1
                next_ivar = None
                next_ivar_armv7 = None
                next_ivar_arm64 = None
                next_ivar_i386 = None
                next_ivar_x86_64 = None
                if index < len(ivars):
                    next_ivar = ivars[index]
                    next_ivar_armv7 = cl_armv7.get_ivar(next_ivar.name)
                    next_ivar_arm64 = cl_arm64.get_ivar(next_ivar.name)
                    next_ivar_i386 = cl_i386.get_ivar(next_ivar.name)
                    next_ivar_x86_64 = cl_x86_64.get_ivar(next_ivar.name)

                # Ivar padding.
                ivar_armv7_padding = 0
                ivar_arm64_padding = 0
                ivar_i386_padding = 0
                ivar_x86_64_padding = 0
                # if next_ivar:
                #     ivar_armv7_padding = next_ivar_armv7.offset - ivar_armv7.offset - ivar_armv7.size
                #     ivar_arm64_padding = next_ivar_arm64.offset - ivar_arm64.offset - ivar_arm64.size
                #     ivar_i386_padding = next_ivar_i386.offset - ivar_i386.offset - ivar_i386.size
                #     ivar_x86_64_padding = next_ivar_x86_64.offset - ivar_x86_64.offset - ivar_x86_64.size

                # Normalized type name.
                type32 = ivar_armv7.ivarType if ivar_armv7 else None
                type64 = ivar_arm64.ivarType if ivar_arm64 else None

                type_name = normalize_type(type32, type64)
                # Split names by new lines.
                first_type_name = u"\n".join(type_name.split(u"\n")[:-1])
                if first_type_name:
                    first_type_name += u"\n"
                last_type_name = type_name.split(u"\n")[-1]
                # Add ivar name to type name.
                type_and_ivar = u"{} {}".format(last_type_name, ivar.name)

                # Offsets values.
                if ivar_armv7_padding:
                    offset_armv7 = u"{0:>3} (0x{0:03X}) / {1:<2} + {2:<2}"\
                        .format(ivar_armv7.offset if ivar_armv7 is not None else -1,
                                ivar_armv7.size if ivar_armv7 is not None else None,
                                ivar_armv7_padding if ivar_armv7 is not None else -1)
                else:
                    offset_armv7 = u"{0:>3} (0x{0:03X}) / {1:<2}"\
                        .format(ivar_armv7.offset if ivar_armv7 is not None else -1,
                                ivar_armv7.size if ivar_armv7 is not None else None)

                if ivar_arm64_padding:
                    offset_arm64 = u"{0:>3} (0x{0:03X}) / {1:<2} + {2:<2}"\
                        .format(ivar_arm64.offset if ivar_arm64 is not None else -1,
                                ivar_arm64.size if ivar_arm64 is not None else None,
                                ivar_arm64_padding if ivar_arm64 is not None else -1)
                else:
                    offset_arm64 = u"{0:>3} (0x{0:03X}) / {1:<2}"\
                        .format(ivar_arm64.offset if ivar_arm64 is not None else -1,
                                ivar_arm64.size if ivar_arm64 is not None else None)

                if ivar_i386_padding:
                    offset_i386 = u"{0:>3} (0x{0:03X}) / {1:<2} + {2:<2}"\
                        .format(ivar_i386.offset if ivar_i386 is not None else -1,
                                ivar_i386.size if ivar_i386 is not None else None,
                                ivar_i386_padding if ivar_i386 is not None else -1)
                else:
                    offset_i386 = u"{0:>3} (0x{0:03X}) / {1:<2}"\
                        .format(ivar_i386.offset if ivar_i386 is not None else -1,
                                ivar_i386.size if ivar_i386 is not None else None)

                if ivar_x86_64_padding:
                    offset_x86_64 = u"{0:>3} (0x{0:03X}) / {1:<2} + {2:<2}"\
                        .format(ivar_x86_64.offset if ivar_x86_64 is not None else -1,
                                ivar_x86_64.size if ivar_x86_64 is not None else None,
                                ivar_x86_64_padding if ivar_x86_64 is not None else -1)
                else:
                    offset_x86_64 = u"{0:>3} (0x{0:03X}) / {1:<2}"\
                        .format(ivar_x86_64.offset if ivar_x86_64 is not None else -1,
                                ivar_x86_64.size if ivar_x86_64 is not None else None)

                output += first_type_name
                output += u"{Name:{name_width}} {ArmV7:{o_width}} {i386:{o_width}} {Arm64:{o_width}} {x86_64:{o_width}}\n"\
                    .format(Name=type_and_ivar,
                            ArmV7=offset_armv7, i386=offset_i386, Arm64=offset_arm64, x86_64=offset_x86_64,
                            name_width=longest_type_and_ivar_length, o_width=offset_width)

        print output


if __name__ == "__main__":
    # Check number of parameters.
    if len(sys.argv) != 2:
        print "Wrong number of parameters"
        exit()

    dump_class(sys.argv[1])
