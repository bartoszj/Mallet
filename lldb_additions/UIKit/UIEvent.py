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

from .. import helpers
from ..common import SummaryBase
from ..Foundation import NSObject


class UIEventSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UIEvent.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIEventSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIEvent"

        self.register_child_value("timestamp", ivar_name="_timestamp",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_timestamp_summary)

    @staticmethod
    def get_timestamp_summary(value):
        return "timeStamp={}".format(value)


def summary_provider(value_obj, internal_dict):
    """
    :param lldb.SBValue value_obj: LLDB value object.
    :param dict internal_dict: Internal LLDB dictionary.
    :return: UIEvent summary.
    :rtype: str
    """
    class_name = helpers.get_object_class_name(value_obj)

    if class_name == "UITouchesEvent":
        import UITouchesEvent
        return helpers.generic_summary_provider(value_obj, internal_dict, UITouchesEvent.UITouchesEventSyntheticProvider)
    else:
        return helpers.generic_summary_provider(value_obj, internal_dict, UIEventSyntheticProvider)
