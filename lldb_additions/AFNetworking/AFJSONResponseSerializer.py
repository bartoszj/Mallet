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
from ..Foundation import NSJSONSerialization
from ..common import SummaryBase
import AFHTTPResponseSerializer


class AFJSONResponseSerializerSyntheticProvider(AFHTTPResponseSerializer.AFHTTPResponseSerializerSyntheticProvider):
    """
    Class representing AFJSONResponseSerializer.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFJSONResponseSerializerSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("reading_options", ivar_name="_readingOptions",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_reading_options_summary)
        self.register_child_value("removes_keys_with_null_values", ivar_name="_removesKeysWithNullValues",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_removes_keys_with_null_values_summary)

    @staticmethod
    def get_reading_options_summary(value):
        text = NSJSONSerialization.get_json_reading_options_text(value)
        if len(text) == 0:
            return None
        return "readingOptions={}".format(text)

    @staticmethod
    def get_removes_keys_with_null_values_summary(value):
        if value:
            return "removesKeysWithNullValues"
        return None

    def summaries_parts(self):
        return [self.reading_options_summary, self.removes_keys_with_null_values_summary] + super(AFJSONResponseSerializerSyntheticProvider, self).summaries_parts()


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFJSONResponseSerializerSyntheticProvider)
