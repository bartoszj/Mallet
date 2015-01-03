#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
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
import SKRequestInternal


class SKRequest_SynthProvider(NSObject.NSObjectSyntheticProvider):
    # Class: SKRequest
    # Super class: NSObject
    # Name:                   armv7                 i386                  arm64                 x86_64
    # id _requestInternal   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKRequest_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKRequest"

        self.request_internal = None
        self.request_internal_provider = None

    @Helpers.save_parameter("request_internal")
    def get_request_internal(self):
        return self.get_child_value("_requestInternal")

    @Helpers.save_parameter("request_internal_provider")
    def get_request_internal_provider(self):
        request_internal = self.get_request_internal()
        return request_internal if request_internal is None else SKRequestInternal.SKRequestInternal_SynthProvider(request_internal, self.internal_dict)

    def summary(self):
        return ""


def SKRequest_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, SKRequest_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKRequest.SKRequest_SummaryProvider \
                            --category StoreKit \
                            SKRequest")
    debugger.HandleCommand("type category enable StoreKit")
