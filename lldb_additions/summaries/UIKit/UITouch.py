#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Bartosz Janda
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

from ...scripts import helpers
from ..Foundation import NSObject
from .. import SummaryBase

UITouchPhaseBegan = 0
UITouchPhaseMoved = 1
UITouchPhaseStationary = 2
UITouchPhaseEnded = 3
UITouchPhaseCancelled = 4


class UITouchSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UITouch.
    """
    def __init__(self, value_obj, internal_dict):
        super(UITouchSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UITouch"

        self.register_child_value("timestamp", ivar_name="_timestamp",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_timestamp_summary)
        self.register_child_value("phase", ivar_name="_phase",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_phase_summary)
        self.register_child_value("saved_phase", ivar_name="_savedPhase",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_saved_phase_summary)
        self.register_child_value("tap_count", ivar_name="_tapCount",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_tap_count_summary)
        self.register_child_value("location_in_window", ivar_name="_locationInWindow",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_location_in_window_summary)
        self.register_child_value("previous_location_in_window", ivar_name="_previousLocationInWindow",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_previous_location_in_window_summary)
        self.register_child_value("pressure", ivar_name="_pressure",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_pressure_summary)
        self.register_child_value("previous_pressure", ivar_name="_previousPressure",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_previous_pressure_summary)

    @staticmethod
    def get_timestamp_summary(value):
        return "timeStamp={}".format(value)

    @staticmethod
    def get_phase_string(value):
        s = "unknown"
        if value == UITouchPhaseBegan:
            s = "began"
        elif value == UITouchPhaseMoved:
            s = "moved"
        elif value == UITouchPhaseStationary:
            s = "stationary"
        elif value == UITouchPhaseEnded:
            s = "ended"
        elif value == UITouchPhaseCancelled:
            s = "cancelled"
        return s

    @staticmethod
    def get_phase_summary(value):
        s = UITouchSyntheticProvider.get_phase_string(value)
        return "phase={}".format(s)

    @staticmethod
    def get_saved_phase_summary(value):
        s = UITouchSyntheticProvider.get_phase_string(value)
        return "savedPhase={}".format(s)

    @staticmethod
    def get_tap_count_summary(value):
        return "tapCount={}".format(value)

    @staticmethod
    def get_location_in_window_summary(value):
        return "locationInWindow={}".format(value)

    @staticmethod
    def get_previous_location_in_window_summary(value):
        return "previousLocationInWindow={}".format(value)

    @staticmethod
    def get_pressure_summary(value):
        if value == 0:
            return None
        return "pressure={}".format(value)

    @staticmethod
    def get_previous_pressure_summary(value):
        if value == 0:
            return None
        return "previousPressure={}".format(value)

    def summary(self):
        summary = SummaryBase.join_summaries(self.location_in_window_summary,
                                             self.phase_summary,
                                             self.tap_count_summary,
                                             self.pressure_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UITouchSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category UIKit \
                            UITouch".format(__name__))
    debugger.HandleCommand("type category enable UIKit")