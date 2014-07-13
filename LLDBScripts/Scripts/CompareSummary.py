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


def breakpoint_compare_summary(frame, bp_loc, dict):
    """
    Breakpoint command used to compare object summary (from obj variable) with string (compare variable).

    This method is used in testing. It compares object summary (from obj variable) with given string
    (compare variable). If they are not equal application execution is stopped.
    """
    # lldb.SBFrame.FindVariable("object")
    obj = frame.FindVariable("object", lldb.eDynamicDontRunTarget)
    obj_summary = obj.GetSummary()

    compare = frame.FindVariable("compare")
    compare_description = compare.GetObjectDescription()

    options = lldb.SBExpressionOptions()
    options.SetIgnoreBreakpoints()

    if obj_summary == compare_description:
        frame.EvaluateExpression("equal = @YES", options)
        # Continue execution.
        return False
    else:
        frame.EvaluateExpression("equal = @NO", options)
        # Break execution.
        return True
