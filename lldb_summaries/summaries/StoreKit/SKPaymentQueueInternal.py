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

from .. import SummaryBase
from ..Foundation import NSObject


class SKPaymentQueueInternalSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing SKPaymentQueueInternal.
    """
    def __init__(self, value_obj, internal_dict):
        super(SKPaymentQueueInternalSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentQueueInternal"

        self.register_child_value("local_transactions", ivar_name="_localTransactions",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_local_transactions_summary)
        self.register_child_value("transactions", ivar_name="_transactions",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_transactions_summary)

    @staticmethod
    def get_local_transactions_summary(value):
        if value != 0:
            return "localTransactions={}".format(value)
        return None

    @staticmethod
    def get_transactions_summary(value):
        if value != 0:
            return "transactions={}".format(value)
        return None

    def summary(self):
        summary = SummaryBase.join_summaries(self.transactions_summary, self.local_transactions_summary)
        return summary
