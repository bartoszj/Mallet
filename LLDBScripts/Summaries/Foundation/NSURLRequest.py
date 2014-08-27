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
import NSObject
import NSURLRequestInternal


class NSURLRequest_SynthProvider(NSObject.NSObject_SynthProvider):
    # NSURLRequest:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSURLRequestInternal *_internal                                         4 = 0x04 / 4            8 = 0x08 / 4

    def __init__(self, value_obj, internal_dict):
        super(NSURLRequest_SynthProvider, self).__init__(value_obj, internal_dict)

        self.request_internal = None
        self.request_internal_provider = None

    def get_request_internal(self):
        if self.request_internal:
            return self.request_internal

        self.request_internal = self.get_value("_internal")
        return self.request_internal

    def get_request_internal_provider(self):
        if self.request_internal_provider:
            return self.request_internal_provider

        request_internal = self.get_request_internal()
        self.request_internal_provider = NSURLRequestInternal.NSURLRequestInternal_SynthProvider(request_internal,
                                                                                                 self.internal_dict)
        return self.request_internal_provider

    def summary(self):
        request_internal_provider = self.get_request_internal_provider()

        request_internal_url = request_internal_provider.get_url()
        request_internal_url_value = request_internal_url.GetSummary()
        request_internal_url_summary = "url={}".format(request_internal_url_value)

        request_internal_method = request_internal_provider.get_method()
        request_internal_method_value = request_internal_method.GetSummary()
        request_internal_method_summary = "method={}".format(request_internal_method_value)

        # Summaries
        summaries = []
        if request_internal_url_value:
            summaries.append(request_internal_url_summary)
        if request_internal_method_value:
            summaries.append(request_internal_method_summary)

        summary = ", ".join(summaries)
        return summary


def NSURLRequest_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, NSURLRequest_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F NSURLRequest.NSURLRequest_SummaryProvider \
                            --category Foundation \
                            NSURLRequest NSMutableURLRequest")
    debugger.HandleCommand("type category enable Foundation")
