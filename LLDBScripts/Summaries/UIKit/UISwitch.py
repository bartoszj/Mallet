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
import summary_helpers
import UIControl


class UISwitch_SynthProvider(UIControl.UIControl_SynthProvider):
    # UISwitch:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # UILongPressGestureRecognizer *_pressGesture                           120 = 0x78 / 4          224 = 0xe0 / 8
    # UIPanGestureRecognizer *_panGesture                                   124 = 0x7c / 4          232 = 0xe8 / 8
    # UIView<_UISwitchInternalViewProtocol> *_control                       128 = 0x80 / 4          240 = 0xf0 / 8
    # BOOL _onStateChangedByLongPressGestureRecognizer                      132 = 0x84 / 1          248 = 0xf8 / 1
    # BOOL _onStateChangedByPanGestureRecognizer                            133 = 0x85 / 1          249 = 0xf9 / 1
    # BOOL _on                                                              134 = 0x86 / 1 + 1      250 = 0xfa / 1 + 5
    # CGFloat _enabledAlpha                                                 136 = 0x88 / 4          256 = 0x100 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UISwitch_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.on = None

        self.update()

    def update(self):
        self.on = None
        super(UISwitch_SynthProvider, self).update()

    def get_on(self):
        if self.on:
            return self.on

        if self.sys_params.is_64_bit:
            offset = 0xfa
        else:
            offset = 0x86

        self.on = self.value_obj.CreateChildAtOffset("on",
                                                     offset,
                                                     self.sys_params.types_cache.char)
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
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UISwitch_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UISwitch.UISwitch_SummaryProvider \
                            --category UIKit \
                            UISwitch")
    debugger.HandleCommand("type category enable UIKit")
