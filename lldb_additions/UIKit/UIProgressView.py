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

from .. import helpers
from ..common import SummaryBase
import UIView


class UIProgressViewSyntheticProvider(UIView.UIViewSyntheticProvider):
    """
    Class representing UIProgressView.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIProgressViewSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIProgressView"

        self.register_child_value("progress", ivar_name="_progress",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_progress_summary)

    @staticmethod
    def get_progress_summary(value):
        return "progress={}".format(SummaryBase.formatted_float(value))

    def summaries_parts(self):
        return [self.progress_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIProgressViewSyntheticProvider)
