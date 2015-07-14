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
from ..Foundation import NSString
from .. import SummaryBase


class AFHTTPResponseSerializerSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing AFHTTPResponseSerializer.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFHTTPResponseSerializerSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("string_encoding", ivar_name="_stringEncoding",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_string_encoding_summary)
        self.register_child_value("acceptable_status_codes", ivar_name="_acceptableStatusCodes")
        self.register_child_value("acceptable_content_types", ivar_name="_acceptableContentTypes",
                                  primitive_value_function=SummaryBase.get_nsset_count_value,
                                  summary_function=self.get_acceptable_content_types_summary)

    @staticmethod
    def get_string_encoding_summary(value):
        if value != NSString.NSUTF8StringEncoding:
            summary = NSString.get_string_encoding_text(value)
            return "stringEncoding={}".format(summary)
        return None

    @staticmethod
    def get_acceptable_content_types_summary(value):
        return "acceptableContentTypes={}".format(value)

    def summaries_parts(self):
        return [self.string_encoding_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFHTTPResponseSerializerSyntheticProvider)
