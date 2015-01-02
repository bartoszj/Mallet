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


class CFURLRequest_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
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
        super(CFURLRequest_SynthProvider, self).__init__(value_obj, internal_dict)

        self.url = None
        self.tmp1_structure = None
        self.method = None

    @Helpers.save_parameter("url")
    def get_url(self):
        if self.is_64bit:
            offset = 0x28
        else:
            offset = 0x14

        return self.get_child_value("url", "NSURL *", offset)

    def get_url_value(self):
        return self.get_summary_value(self.get_url())

    def get_url_summary(self):
        url_value = self.get_url_value()
        if url_value is None:
            return None
        return "url={}".format(url_value)

    @Helpers.save_parameter("tmp1_structure")
    def get_tmp1_structure(self):
        if self.is_64bit:
            offset = 0x50
        else:
            offset = 0x2c

        return self.get_child_value("tmp1", "addr_ptr_type", offset)

    @Helpers.save_parameter("method")
    def get_method(self):
        if self.is_64bit:
            offset = 0x98
        else:
            offset = 0x44

        self.get_tmp1_structure()
        return self.tmp1_structure.CreateChildAtOffset("HTTPMethod", offset, self.get_type("NSString *"))

    def get_method_value(self):
        return self.get_summary_value(self.get_method())

    def get_method_summary(self):
        method_value = self.get_method_value()
        return None if method_value is None else "method={}".format(method_value)

    def summary(self):
        url_summary = self.get_url_summary()
        method_summary = self.get_method_summary()

        # Summaries
        summaries = []
        if url_summary:
            summaries.append(url_summary)
        if method_summary:
            summaries.append(method_summary)

        summary = ", ".join(summaries)
        return summary


def CFURLRequest_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, CFURLRequest_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F CFURLRequest.CFURLRequest_SummaryProvider \
                            --category Foundation \
                            _CFURLRequest")
    debugger.HandleCommand("type category enable Foundation")
