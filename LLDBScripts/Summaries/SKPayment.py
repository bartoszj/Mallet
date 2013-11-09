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


def SKPayment_SummaryProvider(valobj, dict):
    stream = lldb.SBStream()
    valobj.GetExpressionPath(stream)

    # productIdentifier
    product_identifier = valobj.CreateValueFromExpression("productIdentifier",
                                                              "(NSString *)[" + stream.GetData() +
                                                              " productIdentifier]")
    product_identifier_value = product_identifier.GetObjectDescription()
    product_identifier_summary = "@\"{}\"".format(product_identifier_value)

    # quantity
    quantity = valobj.CreateValueFromExpression("quantity",
                                                "(quantity)[" + stream.GetData() +
                                                " quantity]")
    quantity_value = quantity.GetValueAsSigned()
    quantity_summary = "quantity = {}".format(quantity_value)

    # Summaries
    summaries = [product_identifier_summary]
    if quantity_value != 0:
        summaries.append(quantity_summary)

    summary = ", ".join(summaries)
    return summary


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKPayment.SKPayment_SummaryProvider \
                            --category StoreKit \
                            SKPayment SKMutablePayment")
    debugger.HandleCommand("type category enable StoreKit")
