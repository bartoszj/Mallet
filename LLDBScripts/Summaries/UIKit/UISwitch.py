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

import Helpers
import UIControl


class UISwitch_SynthProvider(UIControl.UIControl_SynthProvider):
    # Class: UISwitch
    # Super class: UIControl
    # Protocols: UIGestureRecognizerDelegate, NSCoding
    # Name:                                                armv7                 i386                  arm64                 x86_64
    # UILongPressGestureRecognizer * _pressGesture     120 (0x078) / 4       120 (0x078) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # UIPanGestureRecognizer * _panGesture             124 (0x07C) / 4       124 (0x07C) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # UIView<_UISwitchInternalViewProtocol> * _control 128 (0x080) / 4       128 (0x080) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # BOOL _onStateChangedByLongPressGestureRecognizer 132 (0x084) / 1       132 (0x084) / 1       248 (0x0F8) / 1       248 (0x0F8) / 1
    # BOOL _onStateChangedByPanGestureRecognizer       133 (0x085) / 1       133 (0x085) / 1       249 (0x0F9) / 1       249 (0x0F9) / 1
    # BOOL _on                                         134 (0x086) / 1  + 1  134 (0x086) / 1  + 1  250 (0x0FA) / 1  + 5  250 (0x0FA) / 1  + 5
    # CGFloat _enabledAlpha                            136 (0x088) / 4       136 (0x088) / 4       256 (0x100) / 8       256 (0x100) / 8

    def __init__(self, value_obj, internal_dict):
        super(UISwitch_SynthProvider, self).__init__(value_obj, internal_dict)

        self.on = None

    def get_on(self):
        if self.on:
            return self.on

        self.on = self.get_child_value("_on")
        return self.on

    def summary(self):
        on = self.get_on()
        on_value = on.GetValueAsUnsigned()
        on_summary = "on={}".format("YES" if on_value != 0 else "NO")

        # Summaries
        summaries = [on_summary]

        summary = ", ".join(summaries)
        return summary


def UISwitch_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UISwitch_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UISwitch.UISwitch_SummaryProvider \
                            --category UIKit \
                            UISwitch")
    debugger.HandleCommand("type category enable UIKit")
