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

SKPaymentTransactionStatePurchasing = 0
SKPaymentTransactionStatePurchased = 1
SKPaymentTransactionStateFailed = 2
SKPaymentTransactionStateRestored = 3


class SKPaymentTransaction_SynthProvider(object):
    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKPaymentTransaction_SynthProvider, self).__init__()
        self.value_obj = value_obj
        self.sys_params = sys_params
        self.internal_dict = internal_dict
        if not self.sys_params.types_cache.NSString:
            self.sys_params.types_cache.NSString = self.value_obj.GetTarget().FindFirstType('NSString').GetPointerType()
        self.internal = None
        self.transaction_identifier = None
        self.transaction_state = None
        self.update()

    def update(self):
        self.adjust_for_architecture()
        # _internal (self->_internal)
        self.internal = self.value_obj.GetChildMemberWithName("_internal")
        self.transaction_identifier = None
        self.transaction_state = None

    def adjust_for_architecture(self):
        pass

    # _transactionIdentifier (self->_internal->_transactionIdentifier)
    def get_transaction_identifier(self):
        if not self.transaction_identifier:
            self.transaction_identifier = self.internal.CreateChildAtOffset("transactionIdentifier",
                                                                            7 * self.sys_params.pointer_size,
                                                                            self.sys_params.types_cache.NSString)
        return self.transaction_identifier

    # _transactionState (self->_internal->_transactionState)
    def get_transaction_state(self):
        if not self.transaction_state:
            self.transaction_state = self.internal.CreateChildAtOffset("transactionState",
                                                                       9 * self.sys_params.pointer_size,
                                                                       self.sys_params.types_cache.int)
        return self.transaction_state

    def summary(self):
        #transaction_identifier_value = self.get_transaction_identifier().GetSummary()
        #transaction_identifier_summary = transaction_identifier_value

        transaction_state_value = self.get_transaction_state().GetValueAsUnsigned()
        transaction_state_value_name = "Unknown"
        if transaction_state_value == 0:
            #transaction_state_value_name = "SKPaymentTransactionStatePurchasing"
            transaction_state_value_name = "Purchasing"
        elif transaction_state_value == 1:
            #transaction_state_value_name = "SKPaymentTransactionStatePurchased"
            transaction_state_value_name = "Purchased"
        elif transaction_state_value == 2:
            #transaction_state_value_name = "SKPaymentTransactionStateFailed"
            transaction_state_value_name = "Failed"
        elif transaction_state_value == 3:
            #transaction_state_value_name = "SKPaymentTransactionStateRestored"
            transaction_state_value_name = "Restored"

        transaction_state_summary = "state = {}".format(transaction_state_value_name)

        # Summaries
        summaries = [transaction_state_summary]

        summary = ", ".join(summaries)
        return summary


def SKPaymentTransaction_SummaryProvider(value_obj, internal_dict):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    summary_helpers.update_sys_params(value_obj, class_data.sys_params)
    if wrapper is not None:
        return wrapper.message()

    wrapper = SKPaymentTransaction_SynthProvider(value_obj, class_data.sys_params, internal_dict)
    if wrapper is not None:
        return wrapper.summary()
    return "Summary Unavailable"


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKPaymentTransaction.SKPaymentTransaction_SummaryProvider \
                            --category StoreKit \
                            SKPaymentTransaction")
    debugger.HandleCommand("type category enable StoreKit")
