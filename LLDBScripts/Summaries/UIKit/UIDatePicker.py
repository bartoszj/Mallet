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


class UIDatePicker_SynthProvider(UIControl.UIControl_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UIDatePicker_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIDatePicker"

        self.picker_view = None

    @Helpers.save_parameter("picker_view")
    def get_picker_view(self):
        return self.get_child_value("_pickerView")

    def get_picker_view_value(self):
        return SummaryBase.get_summary_value(self.get_picker_view())

    def get_picker_view_summary(self):
        picker_view_value = self.get_picker_view_value()
        return None if picker_view_value is None else "{}".format(picker_view_value)

    def summary(self):
        picker_view_summary = self.get_picker_view_summary()

        return picker_view_summary


def UIDatePicker_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIDatePicker_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIDatePicker.UIDatePicker_SummaryProvider \
                            --category UIKit \
                            UIDatePicker")
    debugger.HandleCommand("type category enable UIKit")
