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

import summary_helpers
import NSObject
import CFURLRequest


class NSURLRequestInternal_SynthProvider(NSObject.NSObject_SynthProvider):
    # NSURLRequestInternal:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # struct _CFURLRequest *request                                           4 = 0x04 / 4            8 = 0x08 / 4

    def __init__(self, value_obj, sys_params, internal_dict):
        super(NSURLRequestInternal_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.request = None
        self.request_provider = None

        self.update()

    def update(self):
        self.request = None
        super(NSURLRequestInternal_SynthProvider, self).update()

    def get_request(self):
        if self.request:
            return self.request

        if self.sys_params.is_64_bit:
            offset = 0x08
        else:
            offset = 0x04

        self.request = self.value_obj.CreateChildAtOffset("request",
                                                          offset,
                                                          self.sys_params.types_cache.addr_ptr_type)
        return self.request

    def get_request_provider(self):
        if self.request_provider:
            return self.request_provider

        request = self.get_request()
        self.request_provider = CFURLRequest.CFURLRequest_SynthProvider(request, self.sys_params, self.internal_dict)
        return self.request_provider

    def get_url(self):
        request_provider = self.get_request_provider()
        request_url = request_provider.get_url()
        return request_url

    def get_method(self):
        request_provider = self.get_request_provider()
        request_method = request_provider.get_method()
        return request_method

    def summary(self):
        request_url = self.get_url()
        request_url_value = request_url.GetSummary()
        request_url_summary = "url={}".format(request_url_value)

        request_method = self.get_method()
        request_method_value = request_method.GetSummary()
        request_method_summary = "method={}".format(request_method_value)

        # Summaries
        summaries = []
        if request_url_value:
            summaries.append(request_url_summary)
        if request_method_value:
            summaries.append(request_method_summary)

        summary = ", ".join(summaries)
        return summary


def NSURLRequestInternal_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, NSURLRequestInternal_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F NSURLRequestInternal.NSURLRequestInternal_SummaryProvider \
                            --category Foundation \
                            NSURLRequestInternal")
    debugger.HandleCommand("type category enable Foundation")
