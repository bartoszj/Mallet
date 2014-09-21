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
    # Class: UIStepper
    # Super class: UIControl
    # Name:                                    armv7                 i386                  arm64                 x86_64
    # BOOL _isRtoL                         131 (0x083) / 1       124 (0x07C) / 1  + 3  212 (0x0D4) / 1  + 3  220 (0x0DC) / 1  + 3
    # UIImageView * _middleView            132 (0x084) / 4       128 (0x080) / 4       216 (0x0D8) / 8       224 (0x0E0) / 8
    # UIButton * _plusButton               136 (0x088) / 4       132 (0x084) / 4       224 (0x0E0) / 8       232 (0x0E8) / 8
    # UIButton * _minusButton              140 (0x08C) / 4       136 (0x088) / 4       232 (0x0E8) / 8       240 (0x0F0) / 8
    # NSTimer * _repeatTimer               144 (0x090) / 4       140 (0x08C) / 4       240 (0x0F0) / 8       248 (0x0F8) / 8
    # NSInteger _repeatCount               148 (0x094) / 4       144 (0x090) / 4       248 (0x0F8) / 8       256 (0x100) / 8
    # NSMutableDictionary * _dividerImages 152 (0x098) / 4       148 (0x094) / 4       256 (0x100) / 8       264 (0x108) / 8
    # BOOL _continuous                     156 (0x09C) / 1       152 (0x098) / 1       264 (0x108) / 1       272 (0x110) / 1
    # BOOL _autorepeat                     157 (0x09D) / 1       153 (0x099) / 1       265 (0x109) / 1       273 (0x111) / 1
    # BOOL _wraps                          158 (0x09E) / 1  + 1  154 (0x09A) / 1  + 1  266 (0x10A) / 1  + 5  274 (0x112) / 1  + 5
    # double _value                        160 (0x0A0) / 8       156 (0x09C) / 8       272 (0x110) / 8       280 (0x118) / 8
    # double _minimumValue                 168 (0x0A8) / 8       164 (0x0A4) / 8       280 (0x118) / 8       288 (0x120) / 8
    # double _maximumValue                 176 (0x0B0) / 8       172 (0x0AC) / 8       288 (0x120) / 8       296 (0x128) / 8
    # double _stepValue                    184 (0x0B8) / 8       180 (0x0B4) / 8       296 (0x128) / 8       304 (0x130) / 8

    def __init__(self, value_obj, internal_dict):
        super(UIStepper_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIStepper"

        self.value = None
        self.min = None
        self.max = None
        self.step = None

    @Helpers.save_parameter("value")
    def get_value(self):
        return self.get_child_value("_value")

    def get_value_value(self):
        return self.get_float_value(self.get_value())

    def get_value_summary(self):
        value_value = self.get_value_value()
        return None if value_value is None else "value={}".format(self.formatted_float(value_value))

    @Helpers.save_parameter("min")
    def get_min(self):
        return self.get_child_value("_minimumValue")

    def get_min_value(self):
        return self.get_float_value(self.get_min())

    def get_min_summary(self):
        minimum_value = self.get_min_value()
        return None if minimum_value is None else "min={}".format(self.formatted_float(minimum_value))

    @Helpers.save_parameter("max")
    def get_max(self):
        return self.get_child_value("_maximumValue")

    def get_max_value(self):
        return self.get_float_value(self.get_max())

    def get_max_summary(self):
        maximum_value = self.get_max_value()
        return None if maximum_value is None else "max={}".format(self.formatted_float(maximum_value))

    @Helpers.save_parameter("step")
    def get_step(self):
        return self.get_child_value("_stepValue")

    def get_step_value(self):
        return self.get_float_value(self.get_step())

    def get_step_summary(self):
        step_value = self.get_step_value()
        return None if step_value is None else "step={}".format(self.formatted_float(step_value))

    def summary(self):
        value_summary = self.get_value_summary()
        minimum_summary = self.get_min_summary()
        maximum_summary = self.get_max_summary()
        step_value = self.get_step_value()
        step_summary = self.get_step_summary()

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
