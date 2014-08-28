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
    # NSURL *url                                                             16 = 0x10 / 4           32 = 0x20 / 8
    # unknown 24 / 40 bytes                                                  20 = 0x14 / 24          40 = 0x28 / 40
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

    def get_url(self):
        if self.url:
            return self.url

        if self.is_64bit:
            offset = 0x20
        else:
            offset = 0x10

        self.url = self.value_obj.CreateChildAtOffset("url", offset, self.get_type("NSURL *"))
        return self.url

    def get_tmp1_structure(self):
        if self.tmp1_structure:
            return self.tmp1_structure

        if self.is_64bit:
            offset = 0x50
        else:
            offset = 0x2c

        self.tmp1_structure = self.value_obj.CreateChildAtOffset("tmp1", offset, self.get_type("addr_ptr_type"))
        return self.tmp1_structure

    def get_method(self):
        if self.method:
            return self.method

        if self.is_64bit:
            offset = 0x88
        else:
            offset = 0x44

        self.get_tmp1_structure()
        self.method = self.tmp1_structure.CreateChildAtOffset("HTTPMethod", offset, self.get_type("NSString *"))
        return self.method

    def summary(self):
        url = self.get_url()
        url_value = url.GetSummary()
        url_summary = "url={}".format(url_value)

        method = self.get_method()
        method_value = method.GetSummary()
        method_summary = "method={}".format(method_value)

        # Summaries
        summaries = []
        if url_value:
            summaries.append(url_summary)
        if method_value:
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
