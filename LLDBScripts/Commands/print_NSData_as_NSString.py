#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
