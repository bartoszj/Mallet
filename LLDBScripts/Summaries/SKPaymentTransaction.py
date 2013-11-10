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
from helpers import *

SKPaymentTransactionStatePurchasing = 0
SKPaymentTransactionStatePurchased = 1
SKPaymentTransactionStateFailed = 2
SKPaymentTransactionStateRestored = 3


def SKPaymentTransaction_SummaryProvider(valobj, dict):

    # Class data
    class_data, wrapper = get_class_data(valobj)
    if not class_data.sys_params.types_cache.NSString:
        class_data.sys_params.types_cache.NSString = valobj.GetTarget().FindFirstType('NSString').GetPointerType()
    if not class_data.sys_params.types_cache.int:
        class_data.sys_params.types_cache.int = valobj.GetType().GetBasicType(lldb.eBasicTypeInt)

    # _internal (self->_internal)
    internal = valobj.GetChildMemberWithName("_internal")

    # _transactionIdentifier (self->_internal->_transactionIdentifier)
    #transaction_identifier = internal.CreateChildAtOffset("transactionIdentifier",
    #                                                      7 * class_data.sys_params.pointer_size,
    #                                                      class_data.sys_params.types_cache.NSString)
    #transaction_identifier_value = transaction_identifier.GetSummary()
    #transaction_identifier_summary = transaction_identifier_value

    # _transactionState (self->_internal->_transactionState)
    transaction_state = internal.CreateChildAtOffset("transactionState",
                                                     9 * class_data.sys_params.pointer_size,
                                                     class_data.sys_params.types_cache.int)
    transaction_state_value = transaction_state.GetValueAsUnsigned()
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


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKPaymentTransaction.SKPaymentTransaction_SummaryProvider \
                            --category StoreKit \
                            SKPaymentTransaction")
    debugger.HandleCommand("type category enable StoreKit")
