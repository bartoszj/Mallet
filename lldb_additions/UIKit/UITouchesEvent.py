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
import UIInternalEvent


class UITouchesEventSyntheticProvider(UIInternalEvent.UIInternalEventSyntheticProvider):
    """
    Class representing UITouchesEvent.
    """
    def __init__(self, value_obj, internal_dict):
        super(UITouchesEventSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.module_name = "UIKit"
        self.type_name = "UITouchesEvent"

        self.register_child_value("touches", ivar_name="_touches",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_touches_summary)

        self.synthetic_proxy_name = "touches"
        self.synthetic_type = self.SYNTHETIC_PROXY_NAME

    @staticmethod
    def get_touches_summary(value):
        return "touches={}".format(value)

    def summaries_parts(self):
        return [self.touches_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UITouchesEventSyntheticProvider)
