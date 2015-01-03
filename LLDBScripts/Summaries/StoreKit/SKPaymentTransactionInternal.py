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

import NSObject
import Helpers

SKPaymentTransactionStatePurchasing = 0
SKPaymentTransactionStatePurchased = 1
SKPaymentTransactionStateFailed = 2
SKPaymentTransactionStateRestored = 3
SKPaymentTransactionStateDeferred = 4


class SKPaymentTransactionInternal_SynthProvider(NSObject.NSObjectSyntheticProvider):
    # Class: SKPaymentTransactionInternal
    # Super class: NSObject
    # Name:                                           armv7                 i386                  arm64                 x86_64
    # NSArray * _downloads                          4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # NSError * _error                              8 (0x008) / 4         8 (0x008) / 4        16 (0x010) / 8        16 (0x010) / 8
    # SKPaymentTransaction * _originalTransaction  12 (0x00C) / 4        12 (0x00C) / 4        24 (0x018) / 8        24 (0x018) / 8
    # SKPayment * _payment                         16 (0x010) / 4        16 (0x010) / 4        32 (0x020) / 8        32 (0x020) / 8
    # NSString * _temporaryIdentifier              20 (0x014) / 4        20 (0x014) / 4        40 (0x028) / 8        40 (0x028) / 8
    # NSDate * _transactionDate                    24 (0x018) / 4        24 (0x018) / 4        48 (0x030) / 8        48 (0x030) / 8
    # NSString * _transactionIdentifier            28 (0x01C) / 4        28 (0x01C) / 4        56 (0x038) / 8        56 (0x038) / 8
    # NSData * _transactionReceipt                 32 (0x020) / 4        32 (0x020) / 4        64 (0x040) / 8        64 (0x040) / 8
    # NSInteger _transactionState                  36 (0x024) / 4        36 (0x024) / 4        72 (0x048) / 8        72 (0x048) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKPaymentTransactionInternal_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentTransactionInternal"

        self.transaction_date = None
        self.transaction_identifier = None
        self.transaction_receipt = None
        self.transaction_state = None

    @Helpers.save_parameter("transaction_date")
    def get_transaction_date(self):
        return self.get_child_value("_transactionDate")

    @Helpers.save_parameter("transaction_identifier")
    def get_transaction_identifier(self):
        return self.get_child_value("_transactionIdentifier")

    @Helpers.save_parameter("transaction_receipt")
    def get_transaction_receipt(self):
        return self.get_child_value("_transactionReceipt")

    @Helpers.save_parameter("transaction_state")
    def get_transaction_state(self):
        return self.get_child_value("_transactionState")

    def get_transaction_state_value(self):
        return self.get_unsigned_value(self.get_transaction_state())

    def get_transaction_value_text(self):
        transaction_state_value = self.get_transaction_state_value()
        if transaction_state_value is None:
            return None

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
        return transaction_state_value_name

    def get_transaction_value_summary(self):
        transaction_state_value_text = self.get_transaction_value_text()
        return None if transaction_state_value_text is None else "state={}".format(transaction_state_value_text)
