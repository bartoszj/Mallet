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


class UIStepper_SynthProvider(UIControl.UIControl_SynthProvider):
    # UIStepper:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #                                                                                    (+ 4?)
    # BOOL _isRtoL                                                          120 = 0x78 / 1 + 3      220 = 0xdc / 1 + 3
    # UIImageView *_middleView                                              124 = 0x7c / 4          224 = 0xe0 / 8
    # UIButton *_plusButton                                                 128 = 0x80 / 4          232 = 0xe8 / 8
    # UIButton *_minusButton                                                132 = 0x84 / 4          240 = 0xf0 / 8
    # NSTimer *_repeatTimer                                                 136 = 0x88 / 4          248 = 0xf8 / 8
    # NSInteger _repeatCount                                                140 = 0x8c / 4          256 = 0x100 / 8
    # NSMutableDictionary *_dividerImages                                   144 = 0x90 / 4          264 = 0x108 / 8
    # BOOL _continuous                                                      148 = 0x94 / 1          272 = 0x110 / 1
    # BOOL _autorepeat                                                      149 = 0x95 / 1          273 = 0x111 / 1
    # BOOL _wraps                                                           150 = 0x96 / 1 + 1      274 = 0x112 / 1 + 5
    # double _value                                                         152 = 0x98 / 8          280 = 0x118 / 8
    # double _minimumValue                                                  160 = 0xa0 / 8          288 = 0x120 / 8
    # double _maximumValue                                                  168 = 0xa8 / 8          296 = 0x128 / 8
    # double _stepValue                                                     176 = 0xb0 / 8          304 = 0x130 / 8

    def __init__(self, value_obj, internal_dict):
        super(UIStepper_SynthProvider, self).__init__(value_obj, internal_dict)

        self.value = None
        self.min = None
        self.max = None
        self.step = None

    def get_value(self):
        if self.value:
            return self.value

        self.value = self.get_child_value("_value")
        return self.value

    def get_min(self):
        if self.min:
            return self.min

        self.min = self.get_child_value("_minimumValue")
        return self.min

    def get_max(self):
        if self.max:
            return self.max

        self.max = self.get_child_value("_maximumValue")
        return self.max

    def get_step(self):
        if self.step:
            return self.step

        self.step = self.get_child_value("_stepValue")
        return self.step

    def summary(self):
        value = self.get_value()
        value_value = float(value.GetValue())
        value_summary = "value={}".format(value_value)

        minimum = self.get_min()
        minimum_value = float(minimum.GetValue())
        minimum_summary = "min={}".format(minimum_value)

        maximum = self.get_max()
        maximum_value = float(maximum.GetValue())
        maximum_summary = "max={}".format(maximum_value)

        step = self.get_step()
        step_value = float(step.GetValue())
        step_summary = "step={}".format(step_value)

        # Summaries
        summaries = [value_summary]
        if step_value != 1.0:
            summaries.append(step_summary)
        summaries.extend([minimum_summary, maximum_summary])
        summary = ", ".join(summaries)
        return summary


def UIStepper_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIStepper_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIStepper.UIStepper_SummaryProvider \
                            --category UIKit \
                            UIStepper")
    debugger.HandleCommand("type category enable UIKit")
