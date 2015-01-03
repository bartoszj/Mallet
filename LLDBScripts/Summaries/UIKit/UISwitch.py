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


class UISwitch_SynthProvider(UIControl.UIControl_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(UISwitch_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UISwitch"

        self.on = None

    @Helpers.save_parameter("on")
    def get_on(self):
        return self.get_child_value("_on")

    def get_on_value(self):
        return SummaryBase.get_unsigned_value(self.get_on())

    def get_on_summary(self):
        on_value = self.get_on_value()
        return None if on_value is None else "on={}".format("YES" if on_value != 0 else "NO")

    def summary(self):
        on_summary = self.get_on_summary()

        # Summaries
        summaries = [on_summary]

        summary = ", ".join(summaries)
        return summary


def UISwitch_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UISwitch_SynthProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F UISwitch.UISwitch_SummaryProvider \
                            --category UIKit \
                            UISwitch")
    debugger.HandleCommand("type category enable UIKit")
