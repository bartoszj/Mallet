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
    # Class: NSURLRequest
    # Super class: NSObject
    # Protocols: NSSecureCoding, NSCopying, NSMutableCopying
    # Name:                                armv7                 i386                  arm64                 x86_64
    # NSURLRequestInternal * _internal   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8

    def __init__(self, value_obj, internal_dict):
        super(NSURLRequest_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSURLRequest"

        self.request_internal = None
        self.request_internal_provider = None

    @Helpers.save_parameter("request_internal")
    def get_request_internal(self):
        return self.get_child_value("_internal")

    @Helpers.save_parameter("request_internal_provider")
    def get_request_internal_provider(self):
        request_internal = self.get_request_internal()
        return None if request_internal is None else \
            NSURLRequestInternal.NSURLRequestInternal_SynthProvider(request_internal, self.internal_dict)

    def get_url(self):
        request_internal_provider = self.get_request_internal_provider()
        return None if request_internal_provider is None else request_internal_provider.get_url()

    def get_url_value(self):
        return self.get_summary_value(self.get_url())

    def get_url_summary(self):
        url_value = self.get_url_value()
        return None if url_value is None else "url={}".format(url_value)

    def get_method(self):
        request_internal_provider = self.get_request_internal_provider()
        return None if request_internal_provider is None else request_internal_provider.get_method()

    def get_method_value(self):
        return self.get_summary_value(self.get_method())

    def get_method_summary(self):
        method_value = self.get_method_value()
        return None if method_value is None else "method={}".format(method_value)

    def summary(self):
        request_internal_url_summary = self.get_url_summary()
        request_internal_method_summary = self.get_method_summary()

        # Summaries
        summaries = []
        if request_internal_url_summary:
            summaries.append(request_internal_url_summary)
        if request_internal_method_summary:
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
