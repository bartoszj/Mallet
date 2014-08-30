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
import SKPaymentTransactionInternal

SKPaymentTransactionStatePurchasing = 0
SKPaymentTransactionStatePurchased = 1
SKPaymentTransactionStateFailed = 2
SKPaymentTransactionStateRestored = 3
SKPaymentTransactionStateDeferred = 4


class SKPaymentTransaction_SynthProvider(NSObject.NSObject_SynthProvider):
    # Class: SKPaymentTransaction
    # Super class: NSObject
    # Name:            armv7                 i386                  arm64                 x86_64
    # id _internal   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKPaymentTransaction_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentTransaction"

        self.internal = None
        self.internal_provider = None

    def get_internal(self):
        if self.internal:
            return self.internal

        self.internal = self.get_child_value("_internal")
        return self.internal

    def get_internal_provider(self):
        if self.internal_provider:
            return self.internal_provider

        internal = self.get_internal()
        self.internal_provider = SKPaymentTransactionInternal.SKPaymentTransactionInternal_SynthProvider(internal, self.internal_dict)
        return self.internal_provider

    def summary(self):
        # transaction_identifier_value = self.get_internal_provider().get_transaction_identifier().GetSummary()
        # transaction_identifier_summary = transaction_identifier_value

        transaction_state_value = self.get_internal_provider().get_transaction_state().GetValueAsUnsigned()
        transaction_state_value_name = "Unknown"
        if transaction_state_value == SKPaymentTransactionStatePurchasing:
            transaction_state_value_name = "Purchasing"
        elif transaction_state_value == SKPaymentTransactionStatePurchased:
            transaction_state_value_name = "Purchased"
        elif transaction_state_value == SKPaymentTransactionStateFailed:
            transaction_state_value_name = "Failed"
        elif transaction_state_value == SKPaymentTransactionStateRestored:
            transaction_state_value_name = "Restored"
        elif transaction_state_value == SKPaymentTransactionStateDeferred:
            transaction_state_value_name = "Deferred"

        transaction_state_summary = "state={}".format(transaction_state_value_name)

        # Summaries
        summaries = [transaction_state_summary]

        summary = ", ".join(summaries)
        return summary


def SKPaymentTransaction_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, SKPaymentTransaction_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKPaymentTransaction.SKPaymentTransaction_SummaryProvider \
                            --category StoreKit \
                            SKPaymentTransaction")
    debugger.HandleCommand("type category enable StoreKit")
