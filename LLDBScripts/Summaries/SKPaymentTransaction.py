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

SKPaymentTransactionStatePurchasing = 0
SKPaymentTransactionStatePurchased = 1
SKPaymentTransactionStateFailed = 2
SKPaymentTransactionStateRestored = 3


def SKPaymentTransaction_SummaryProvider(valobj, dict):
    stream = lldb.SBStream()
    valobj.GetExpressionPath(stream)

    # transactionIdentifier
    #transaction_identifier = valobj.CreateValueFromExpression("transactionIdentifier",
    #                                                          "(NSString *)[" + stream.GetData() +
    #                                                          " transactionIdentifier]")
    #transaction_identifier_value = transaction_identifier.GetObjectDescription()
    #transaction_identifier_summary = "@\"{}\"".format(transaction_identifier_value)

    # transactionState
    transaction_state = valobj.CreateValueFromExpression("transactionState",
                                                         "(SKPaymentTransactionState)[" + stream.GetData() +
                                                         " transactionState]")
    transaction_state_value = transaction_state.GetValueAsUnsigned()
    if transaction_state_value == 0:
        #transaction_state_value_name = "SKPaymentTransactionStatePurchasing"
        transaction_state_value_name = "purchasing"
    elif transaction_state_value == 1:
        #transaction_state_value_name = "SKPaymentTransactionStatePurchased"
        transaction_state_value_name = "purchased"
    elif transaction_state_value == 2:
        #transaction_state_value_name = "SKPaymentTransactionStateFailed"
        transaction_state_value_name = "failed"
    elif transaction_state_value == 3:
        #transaction_state_value_name = "SKPaymentTransactionStateRestored"
        transaction_state_value_name = "restored"

    transaction_state_summary = "state = {}".format(transaction_state_value_name)

    # transactionDate
    #transaction_date = valobj.CreateValueFromExpression("transactionDate",
    #                                                     "(NSDate *)[" + stream.GetData() +
    #                                                     " transactionDate]")
    #transaction_date_value = transaction_date.GetObjectDescription()
    #transaction_date_summary = transaction_date_value

    # Summaries
    summaries = [transaction_state_summary]

    summary = ", ".join(summaries)
    return summary


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKPaymentTransaction.SKPaymentTransaction_SummaryProvider \
                            --category StoreKit \
                            SKPaymentTransaction")
    debugger.HandleCommand("type category enable StoreKit")
