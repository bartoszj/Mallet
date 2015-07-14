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
from ..Foundation import NSPropertyListSerialization
from .. import SummaryBase
import AFHTTPRequestSerializer


class AFPropertyListRequestSerializerSyntheticProvider(AFHTTPRequestSerializer.AFHTTPRequestSerializerSyntheticProvider):
    """
    Class representing AFPropertyListRequestSerializer.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFPropertyListRequestSerializerSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("format", ivar_name="_format",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_format_summary)
        self.register_child_value("write_options", ivar_name="_writeOptions",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_write_options_summary)

    @staticmethod
    def get_format_summary(value):
        text = NSPropertyListSerialization.get_format_text(value)
        if len(text) == 0:
            return None
        return "format={}".format(text)

    @staticmethod
    def get_write_options_summary(value):
        text = NSPropertyListSerialization.get_mutability_text(value)
        if len(text) == 0:
            return None
        return "writeOptions={}".format(text)

    def summaries_parts(self):
        return [self.format_summary, self.write_options_summary] + super(AFPropertyListRequestSerializerSyntheticProvider, self).summaries_parts()


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFPropertyListRequestSerializerSyntheticProvider)
