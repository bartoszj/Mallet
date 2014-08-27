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

import summary_helpers
import UIControl


class UIDatePicker_SynthProvider(UIControl.UIControl_SynthProvider):
    # UIDatePicker:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # _UIDatePickerView *_pickerView                                        120 = 0x78 / 4          224 = 0xe0 / 8
    # BOOL _useCurrentDateDuringDecoding                                    124 = 0x7c / 1          232 = 0xe8 / 1

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UIDatePicker_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        if not self.sys_params.types_cache.UIDatePickerView:
            self.sys_params.types_cache.UIDatePickerView = self.value_obj.GetTarget().\
                FindFirstType('_UIDatePickerView').GetPointerType()

        self.picker_view = None

        self.update()

    def update(self):
        self.picker_view = None
        super(UIDatePicker_SynthProvider, self).update()

    def get_picker_view(self):
        if self.picker_view:
            return self.picker_view

        if self.sys_params.is_64_bit:
            offset = 0xe0
        else:
            offset = 0x78

        self.picker_view = self.value_obj.CreateChildAtOffset("pickerView",
                                                              offset,
                                                              self.sys_params.types_cache.UIDatePickerView)
        return self.picker_view

    def summary(self):
        picker_view = self.get_picker_view()
        picker_view_summary = picker_view.GetSummary()

        return picker_view_summary


def UIDatePicker_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIDatePicker_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIDatePicker.UIDatePicker_SummaryProvider \
                            --category UIKit \
                            UIDatePicker")
    debugger.HandleCommand("type category enable UIKit")
