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

import lldb
import objc_runtime
import summary_helpers

statistics = lldb.formatters.metrics.Metrics()
statistics.add_metric('invalid_isa')
statistics.add_metric('invalid_pointer')
statistics.add_metric('unknown_class')
statistics.add_metric('code_notrun')


class SKRequest_SynthProvider(object):
    # SKRequest:
    # Offset / size                                 32bit:              64bit:
    #
    # Class isa                                      0 = 0x00 / 4        0 = 0x00 / 8
    # SKRequestInternal *_requestInternal            4 = 0x04 / 4        8 = 0x08 / 8

    # SKRequestInternal:
    # Offset / size                                 32bit:              64bit:
    #
    # Class isa                                      0 = 0x00 / 4        0 = 0x00 / 8
    # int _backgroundTaskIdentifier                  4 = 0x04 / 4        8 = 0x08 / 4 + 4
    # SKPaymentQueueClient *_client                  8 = 0x08 / 4       16 = 0x10 / 8
    # SKXPCConnection *_connection                  12 = 0x0c / 4       24 = 0x18 / 8
    # id<SKRequestDelegate> _delegate               16 = 0x10 / 4       32 = 0x20 / 8
    # int _state                                    20 = 0x14 / 4       40 = 0x28 / 4

    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKRequest_SynthProvider, self).__init__()
        self.value_obj = value_obj
        self.sys_params = sys_params
        self.internal_dict = internal_dict

        self.request_internal = None
        self.update()

    def update(self):
        self.adjust_for_architecture()
        # _requestInternal (self->_requestInternal)
        self.request_internal = self.value_obj.GetChildMemberWithName("_requestInternal")

    def adjust_for_architecture(self):
        pass

    def summary(self):
        return ""


def SKRequest_SummaryProvider(value_obj, internal_dict):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    summary_helpers.update_sys_params(value_obj, class_data.sys_params)
    if wrapper is not None:
        return wrapper.message()

    wrapper = SKRequest_SynthProvider(value_obj, class_data.sys_params, internal_dict)
    if wrapper is not None:
        return wrapper.summary()
    return "Summary Unavailable"


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKRequest.SKRequest_SummaryProvider \
                            --category StoreKit \
                            SKRequest")
    debugger.HandleCommand("type category enable StoreKit")
