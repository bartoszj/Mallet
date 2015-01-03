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


class SKPaymentQueueInternal_SynthProvider(NSObject.NSObjectSyntheticProvider):
    # Class: SKPaymentQueueInternal
    # Super class: NSObject
    # Name:                                     armv7                 i386                  arm64                 x86_64
    # BOOL _checkedIn                         4 (0x004) / 1  + 3    4 (0x004) / 1  + 3    8 (0x008) / 1  + 7    8 (0x008) / 1  + 7
    # SKPaymentQueueClient * _client          8 (0x008) / 4         8 (0x008) / 4        16 (0x010) / 8        16 (0x010) / 8
    # BOOL _isRefreshing                     12 (0x00C) / 1  + 3   12 (0x00C) / 1  + 3   24 (0x018) / 1  + 7   24 (0x018) / 1  + 7
    # NSMutableArray * _localTransactions    16 (0x010) / 4        16 (0x010) / 4        32 (0x020) / 8        32 (0x020) / 8
    # struct __CFArray * _observers          20 (0x014) / 4        20 (0x014) / 4        40 (0x028) / 8        40 (0x028) / 8
    # SKXPCConnection * _requestConnection   24 (0x018) / 4        24 (0x018) / 4        48 (0x030) / 8        48 (0x030) / 8
    # SKXPCConnection * _responseConnection  28 (0x01C) / 4        28 (0x01C) / 4        56 (0x038) / 8        56 (0x038) / 8
    # BOOL _restoreFinishedDuringRefresh     32 (0x020) / 1        32 (0x020) / 1        64 (0x040) / 1        64 (0x040) / 1
    # BOOL _restoringCompletedTransactions   33 (0x021) / 1  + 2   33 (0x021) / 1  + 2   65 (0x041) / 1  + 6   65 (0x041) / 1  + 6
    # NSMutableArray * _transactions         36 (0x024) / 4        36 (0x024) / 4        72 (0x048) / 8        72 (0x048) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKPaymentQueueInternal_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentQueueInternal"

        self.local_transactions = None
        self.transactions = None

    @Helpers.save_parameter("local_transactions")
    def get_local_transactions(self):
        return self.get_child_value("_localTransactions")

    def get_local_transactions_value(self):
        return self.get_signed_value(self.get_local_transactions())

    def get_local_transactions_summary(self):
        local_transactions_value = self.get_local_transactions_value()
        return None if local_transactions_value is None else "localTransactions={}".format(local_transactions_value)

    @Helpers.save_parameter("transactions")
    def get_transactions(self):
        return self.get_child_value("_transactions")

    def get_transactions_value(self):
        return self.get_count_value(self.get_transactions())

    def get_transactions_summary(self):
        transactions_value = self.get_transactions_value()
        return None if transactions_value is None else "transactions={}".format(transactions_value)
