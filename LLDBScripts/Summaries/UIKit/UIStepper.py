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
import SummaryBase
import UIControl


class UIStepper_SynthProvider(UIControl.UIControl_SynthProvider):
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
        return SummaryBase.get_float_value(self.get_value())

    def get_value_summary(self):
        value_value = self.get_value_value()
        return None if value_value is None else "value={}".format(SummaryBase.formatted_float(value_value))

    @Helpers.save_parameter("min")
    def get_min(self):
        return self.get_child_value("_minimumValue")

    def get_min_value(self):
        return SummaryBase.get_float_value(self.get_min())

    def get_min_summary(self):
        minimum_value = self.get_min_value()
        return None if minimum_value is None else "min={}".format(SummaryBase.formatted_float(minimum_value))

    @Helpers.save_parameter("max")
    def get_max(self):
        return self.get_child_value("_maximumValue")

    def get_max_value(self):
        return SummaryBase.get_float_value(self.get_max())

    def get_max_summary(self):
        maximum_value = self.get_max_value()
        return None if maximum_value is None else "max={}".format(SummaryBase.formatted_float(maximum_value))

    @Helpers.save_parameter("step")
    def get_step(self):
        return self.get_child_value("_stepValue")

    def get_step_value(self):
        return SummaryBase.get_float_value(self.get_step())

    def get_step_summary(self):
        step_value = self.get_step_value()
        return None if step_value is None else "step={}".format(SummaryBase.formatted_float(step_value))

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
