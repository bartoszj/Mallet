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

from ...scripts import helpers
from ..Foundation import NSObject
import SKPaymentTransactionInternal


class SKPaymentTransactionSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing SKPaymentTransaction.
    """
    def __init__(self, value_obj, internal_dict):
        super(SKPaymentTransactionSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentTransaction"

        self.register_child_value("internal", ivar_name="_internal",
                                  provider_class=SKPaymentTransactionInternal.SKPaymentTransactionInternalSyntheticProvider,
                                  summary_function=self.get_internal_summary)

    @staticmethod
    def get_internal_summary(provider):
        """
        SKPaymentTransactionInternal summary.

        :param SKPaymentTransactionInternal.SKPaymentTransactionInternalSyntheticProvider provider: SKPaymentTransactionInternal provider.
        :return: SKPaymentTransactionInternal summary.
        :rtype: str
        """
        return provider.summary()

    def summary(self):
        return self.internal_summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, SKPaymentTransactionSyntheticProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKPaymentTransaction.summary_provider \
                            --category StoreKit \
                            SKPaymentTransaction")
    debugger.HandleCommand("type category enable StoreKit")
