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


def SKPayment_SummaryProvider(valobj, dict):

    # Class data
    class_data, wrapper = get_class_data(valobj)
    if not class_data.sys_params.types_cache.NSString:
        class_data.sys_params.types_cache.NSString = valobj.GetTarget().FindFirstType('NSString').GetPointerType()


    # _internal (self->_internal)
    internal = valobj.GetChildMemberWithName("_internal")

    # _applicationUsername (self->_internal->_applicationUsername)
    application_username = internal.CreateChildAtOffset("applicationUsername",
                                                        1 * class_data.sys_params.pointer_size,
                                                        class_data.sys_params.types_cache.NSString)
    application_username_value = application_username.GetSummary()
    application_username_summary = None
    if application_username_value:
        application_username_summary = "applicationUsername = {}".format(application_username_value[2:-1])

    # _productIdentifier (self->_internal->_productIdentifier)
    product_identifier = internal.CreateChildAtOffset("productIdentifier",
                                                      2 * class_data.sys_params.pointer_size,
                                                      class_data.sys_params.types_cache.NSString)
    product_identifier_value = product_identifier.GetSummary()
    product_identifier_summary = product_identifier_value

    # _quantity (self->_internal->_quantity)
    quantity = internal.CreateChildAtOffset("quantity",
                                            3 * class_data.sys_params.pointer_size,
                                            class_data.sys_params.types_cache.int)
    quantity_value = quantity.GetValueAsSigned()
    quantity_summary = "quantity = {}".format(quantity_value)

    # Summaries
    summaries = [product_identifier_summary]
    if application_username_value:
        summaries.append(application_username_summary)
    if quantity_value != 1:
        summaries.append(quantity_summary)

    summary = ", ".join(summaries)
    return summary


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKPayment.SKPayment_SummaryProvider \
                            --category StoreKit \
                            SKPayment SKMutablePayment")
    debugger.HandleCommand("type category enable StoreKit")
