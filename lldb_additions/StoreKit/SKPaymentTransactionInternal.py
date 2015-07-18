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

from ..common import SummaryBase
from ..Foundation import NSObject

SKPaymentTransactionStatePurchasing = 0
SKPaymentTransactionStatePurchased = 1
SKPaymentTransactionStateFailed = 2
SKPaymentTransactionStateRestored = 3
SKPaymentTransactionStateDeferred = 4


class SKPaymentTransactionInternalSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing SKPaymentTransactionInternal.
    """
    def __init__(self, value_obj, internal_dict):
        super(SKPaymentTransactionInternalSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentTransactionInternal"

        self.register_child_value("transaction_date", ivar_name="_transactionDate",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_transaction_date_summary)
        self.register_child_value("transaction_identifier", ivar_name="_transactionIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_transaction_identifier_summary)
        self.register_child_value("transaction_receipt", ivar_name="_transactionIdentifier")
        self.register_child_value("transaction_state", ivar_name="_transactionState",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_transaction_state_summary)

    @staticmethod
    def get_transaction_date_summary(value):
        return "date={}".format(value)

    @staticmethod
    def get_transaction_identifier_summary(value):
        return "identifier={}".format(value)

    @staticmethod
    def get_transaction_state_summary(value):
        name = "Unknown"
        if value == SKPaymentTransactionStatePurchasing:
            name = "Purchasing"
        elif value == SKPaymentTransactionStatePurchased:
            name = "Purchased"
        elif value == SKPaymentTransactionStateFailed:
            name = "Failed"
        elif value == SKPaymentTransactionStateRestored:
            name = "Restored"
        elif value == SKPaymentTransactionStateDeferred:
            name = "Deferred"
        return "state={}".format(name)

    def summaries_parts(self):
        return [self.transaction_state_summary]
