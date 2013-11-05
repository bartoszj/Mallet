#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
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

import lldb


def print_NSData_as_NSString_command(debugger, command, result, internal_dict):
    """
    Overview:

    A command to print NSData object as NSString.

    Example:

    pds data
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()

    if not target.IsValid() or not process.IsValid():
        result.SetError("Unable to get target/process")
        return

    options = lldb.SBExpressionOptions()
    options.SetIgnoreBreakpoints()

    print_command = "(NSString *)[[NSString alloc] initWithData:({0!s}) encoding:4]".format(command)
    if frame.IsValid():
        data = frame.EvaluateExpression(print_command, options)
        data_description = data.GetObjectDescription()

        print >> result, data_description
    else:
        print "Invalid frame."


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f print_NSData_as_NSString.print_NSData_as_NSString_command pds')
