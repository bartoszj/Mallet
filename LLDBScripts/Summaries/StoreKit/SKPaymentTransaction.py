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

import summary_helpers
import NSObject

SKPaymentTransactionStatePurchasing = 0
SKPaymentTransactionStatePurchased = 1
SKPaymentTransactionStateFailed = 2
SKPaymentTransactionStateRestored = 3


class SKPaymentTransaction_SynthProvider(NSObject.NSObject_SynthProvider):
    # SKPaymentTransaction:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # SKPaymentTransactionInternal *_internal                                 4 = 0x04 / 4            8 = 0x08 / 8

    # SKPaymentTransactionInternal:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSArray *_downloads                                                     4 = 0x04 / 4            8 = 0x08 / 8
    # NSError *_error                                                         8 = 0x08 / 4           16 = 0x08 / 8
    # SKPaymentTransaction *_originalTransaction                             12 = 0x0c / 4           24 = 0x08 / 8
    # SKPayment *_payment                                                    16 = 0x10 / 4           32 = 0x08 / 8
    # NSString *_temporaryIdentifier                                         20 = 0x14 / 4           40 = 0x08 / 8
    # NSDate *_transactionDate                                               24 = 0x18 / 4           48 = 0x08 / 8
    # NSString *_transactionIdentifier                                       28 = 0x1c / 4           56 = 0x08 / 8
    # NSData *_transactionReceipt                                            32 = 0x20 / 4           64 = 0x08 / 8
    # NSInteger _transactionState                                            36 = 0x24 / 4           72 = 0x08 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKPaymentTransaction_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.internal = None
        self.transaction_identifier = None
        self.transaction_state = None

        self.update()

    def update(self):
        # _internal (self->_internal)
        self.internal = self.value_obj.GetChildMemberWithName("_internal")
        self.transaction_identifier = None
        self.transaction_state = None
        super(SKPaymentTransaction_SynthProvider, self).update()

    # _transactionIdentifier (self->_internal->_transactionIdentifier)
    def get_transaction_identifier(self):
        if self.transaction_identifier:
            return self.transaction_identifier

        if self.internal:
            self.transaction_identifier = self.internal.CreateChildAtOffset("transactionIdentifier",
                                                                            7 * self.sys_params.pointer_size,
                                                                            self.sys_params.types_cache.NSString)
        return self.transaction_identifier

    # _transactionState (self->_internal->_transactionState)
    def get_transaction_state(self):
        if self.transaction_state:
            return self.transaction_state

        if self.internal:
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

        transaction_state_summary = "state={}".format(transaction_state_value_name)

        # Summaries
        summaries = [transaction_state_summary]

        summary = ", ".join(summaries)
        return summary


def SKPaymentTransaction_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, SKPaymentTransaction_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKPaymentTransaction.SKPaymentTransaction_SummaryProvider \
                            --category StoreKit \
                            SKPaymentTransaction")
    debugger.HandleCommand("type category enable StoreKit")
