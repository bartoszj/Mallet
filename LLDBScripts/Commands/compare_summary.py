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

import lldb


def compare_summary(debugger, command, result, internal_dict):
    args = command.split(" ")
    if len(args) != 4:
        result.SetError("Not enough arguments.")
        return

    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()

    obj_name = args[0]
    obj_val = frame.FindVariable(obj_name, lldb.eDynamicDontRunTarget)
    # obj_val = frame.FindVariable(obj_name, lldb.eDynamicCanRunTarget)
    obj_summary = obj_val.GetSummary()

    class_name = args[1]
    class_val = frame.FindVariable(class_name)
    class_type_name = class_val.GetSummary()[2:-1]
    class_type = target.FindFirstType(class_type_name).GetPointerType()

    # casted_val = obj_val.Cast(class_type)
    casted_val = obj_val.CreateValueFromExpression("casted",
                                                   "({}){}".format(class_type_name, obj_name))
    casted_summary = casted_val.GetSummary()
    # summary = obj_summary
    summary = casted_summary

    compare_name = args[2]
    compare_val = frame.FindVariable(compare_name)
    compare_description = compare_val.GetObjectDescription()

    result_name = args[3]

    options = lldb.SBExpressionOptions()
    options.SetIgnoreBreakpoints()
    if summary == compare_description:
        frame.EvaluateExpression("{} = @YES".format(result_name), options)
    else:
        print >> result, "object: {}".format(summary)
        frame.EvaluateExpression("{} = @NO".format(result_name), options)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f compare_summary.compare_summary compare_summary')