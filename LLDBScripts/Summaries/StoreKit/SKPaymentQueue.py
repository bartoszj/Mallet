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
import SKPaymentQueueInternal


class SKPaymentQueue_SynthProvider(NSObject.NSObjectSyntheticProvider):
    # Class: SKPaymentQueue
    # Super class: NSObject
    # Name:            armv7                 i386                  arm64                 x86_64
    # id _internal   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKPaymentQueue_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentQueue"

        self.internal = None
        self.internal_provider = None

    @Helpers.save_parameter("internal")
    def get_internal(self):
        return self.get_child_value("_internal")

    @Helpers.save_parameter("internal_provider")
    def get_internal_provider(self):
        internal = self.get_internal()
        return None if internal is None else SKPaymentQueueInternal.SKPaymentQueueInternal_SynthProvider(internal, self.internal_dict)

    def get_local_transactions_value(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_local_transactions_value()

    def get_local_transactions_summary(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_local_transactions_summary()

    def get_transactions_value(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_transactions_value()

    def get_transactions_summary(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_transactions_summary()

    def summary(self):
        local_transactions_count = self.get_local_transactions_value()
        local_transactions_summary = self.get_local_transactions_summary()

        transactions_count = self.get_local_transactions_value()
        transactions_summary = self.get_local_transactions_summary()

        summaries = []
        if local_transactions_count != 0:
            summaries.append(local_transactions_summary)
        if transactions_count != 0:
            summaries.append(transactions_summary)

        summary = ", ".join(summaries)
        return summary


def SKPaymentQueue_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, SKPaymentQueue_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKPaymentQueue.SKPaymentQueue_SummaryProvider \
                            --category StoreKit \
                            SKPaymentQueue")
    debugger.HandleCommand("type category enable StoreKit")
