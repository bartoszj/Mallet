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
    """
    Compares object summary with predefined results and sets results to defined variable.

    compare_summary object type summary equal

    - object: Object which summary should be compared.
    - type: Type of object (as string).
    - summary: Predefined summary to compare
    - equal: Variable of type NSNumber to which results will be set.

    :param lldb.SBDebugger debugger: LLDB debugger.
    :param str command: Command attributes.
    :param lldb.SBCommandReturnObject result: Results.
    :param dict internal_dict: Internal LLDB dictionary.
    """
    args = command.split(" ")
    if len(args) != 4:
        result.SetError("Not enough arguments.")
        return

    target = debugger.GetSelectedTarget()
    """:type: lldb.SBTarget"""
    process = target.GetProcess()
    """:type: lldb.SBProcess"""
    thread = process.GetSelectedThread()
    """:type: lldb.SBThread"""
    frame = thread.GetSelectedFrame()
    """:type: lldb.SBFrame"""

    # Object name.
    obj_name = args[0]
    """:type: str"""
    obj_val = frame.FindVariable(obj_name, lldb.eDynamicDontRunTarget)
    """:type: lldb.SBValue"""
    # obj_val = frame.FindVariable(obj_name, lldb.eDynamicCanRunTarget)
    # obj_summary = obj_val.GetSummary()

    # Class name.
    class_name = args[1]
    """:type: str"""
    class_val = frame.FindVariable(class_name)
    """:type: lldb.SBValue"""
    class_type_name = class_val.GetSummary()[2:-1]
    """:type: str"""
    # class_type = target.FindFirstType(class_type_name).GetPointerType()

    # Casting object to given class.
    # casted_val = obj_val.Cast(class_type)
    casted_val = obj_val.CreateValueFromExpression("casted", "({}){}".format(class_type_name, obj_name))
    """:type: lldb.SBValue"""
    casted_val = casted_val.GetDynamicValue(lldb.eDynamicDontRunTarget)
    """:type: lldb.SBValue"""
    # casted_val = casted_val.GetDynamicValue(lldb.eDynamicCanRunTarget)

    # Summary.
    casted_summary = casted_val.GetSummary()
    """:type: str"""
    # summary = obj_summary
    summary = casted_summary

    # Compare string.
    compare_name = args[2]
    """:type: str"""
    compare_val = frame.FindVariable(compare_name)
    """:type: lldb.SBValue"""
    compare_description = compare_val.GetObjectDescription()
    """:type: str"""

    # Result object.
    result_name = args[3]
    """:type: str"""

    # Debug printing:
    # print("object name: {}".format(obj_name))
    # print("object value: {}".format(obj_val))
    # print("object summary: {}".format(obj_summary))
    # print("")
    # print("class name: {}".format(class_name))
    # print("class value: {}".format(class_val))
    # print("class type name: {}".format(class_type_name))
    # print("")
    # print("casted object value: {}".format(casted_val))
    # print("casted object summary: {}".format(casted_summary))
    # print("")
    # print("compare name: {}".format(compare_name))
    # print("compare value: {}".format(compare_val))
    # print("compare description: {}".format(compare_description))
    # print("")
    # print("results name: {}".format(result_name))

    # Comparison.
    options = lldb.SBExpressionOptions()
    options.SetIgnoreBreakpoints()
    if summary == compare_description:
        frame.EvaluateExpression("{} = @1".format(result_name), options)
    else:
        print >> result, "object: {}\nshould be: {}".format(summary, compare_description)
        frame.EvaluateExpression("{} = @0".format(result_name), options)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f compare_summary.compare_summary compare_summary')
