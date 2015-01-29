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

from ...scripts import helpers
from .. import SummaryBase


class CFURLRequestSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing _CFURLRequest structure.
    """
    # _CFURLRequest:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # unknown 16 / 32 bytes                                                   0 = 0x00 / 16           0 = 0x00 / 32
    # NSURL *url                                                             20 = 0x14 / 4           40 = 0x28 / 8
    # unknown 24 / 40 bytes                                                  20 = 0x14 / 24          48 = 0x28 / 40
    # struct _tmp1 *tmp1                                                     44 = 0x2c / 4           80 = 0x50 / 8

    # struct _tmp1 {
    #     unknown 68 / 136 bytes                                              0 = 0x00 / 68           0 = 0x00 / 136
    #     NSString *HTTPMethod                                               68 = 0x44 / 4          136 = 0x88 / 8
    # }

    def __init__(self, value_obj, internal_dict):
        """
        :param lldb.SBValue value_obj: LLDB variable to compute summary.
        :param dict internal_dict: Internal LLDB dictionary.
        """
        super(CFURLRequestSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            url_offset = 0x28
            tmp1_offset = 0x58
        else:
            url_offset = 0x14
            tmp1_offset = 0x30

        self.register_child_value("url", type_name="NSURL *", offset=url_offset,
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_url_summary)
        self.register_child_value("tmp1", type_name="addr_ptr_type", offset=tmp1_offset)

        self.method = None

    @staticmethod
    def get_url_summary(value):
        return "url={}".format(value)

    @helpers.save_parameter("method")
    def get_method(self):
        if self.is_64bit:
            offset = 0x88
        else:
            offset = 0x44

        return self.tmp1.CreateChildAtOffset("HTTPMethod", offset, self.get_type("NSString *"))

    def get_method_value(self):
        return SummaryBase.get_summary_value(self.get_method())

    def get_method_summary(self):
        method_value = self.get_method_value()
        return None if method_value is None else "method={}".format(method_value)

    def summary(self):
        summary = SummaryBase.join_summaries(self.url_summary, self.get_method_summary())
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, CFURLRequestSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category CFNetwork \
                            _CFURLRequest".format(__name__))
    debugger.HandleCommand("type category enable CFNetwork")
