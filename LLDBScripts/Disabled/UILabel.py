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

from UIView import *


# Text
def UILabel_text(valobj, stream):
    text = valobj.CreateValueFromExpression("text", "(NSString *)[" + stream.GetData() + " text]")
    return text


def UILabel_SummaryProvider(valobj, dict):
    stream = lldb.SBStream()
    valobj.GetExpressionPath(stream)

    # Text
    text = UILabel_text(valobj, stream)
    text_value = text.GetObjectDescription()
    text_summary = "text = \"{}\"".format(text_value)

    # Frame
    (x, y, width, height) = UIView_frame(valobj, stream)
    frame_summary = "frame = ({} {}; {} {})".format(x.GetValue(), y.GetValue(), width.GetValue(), height.GetValue())

    # Alpha
    alpha = UIView_alpha(valobj, stream)
    alpha_value = float(alpha.GetValue())
    alpha_summary = "alpha = {:4.2f}".format(alpha_value)

    # Hidden
    hidden = UIView_hidden(valobj, stream)
    hidden_value = hidden.GetValueAsUnsigned()
    hidden_summary = "hidden = {}".format("YES" if hidden_value == 1 else "NO")

    # Summary
    summaries = [frame_summary]
    if len(text_value) > 0:
        summaries.insert(0, text_summary)
    if alpha_value != 1.0:
        summaries.append(alpha_summary)
    if hidden_value != 0:
        summaries.append(hidden_summary)

    summary = ", ".join(summaries)

    return summary


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UILabel.UILabel_SummaryProvider \
                            --category UIKit \
                            UILabel")
    debugger.HandleCommand("type category enable UIKit")