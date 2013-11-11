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
import NSSet
from helpers import *


def SKProductsRequest_SummaryProvider(valobj, dict):

    # Class data
    class_data, wrapper = get_class_data(valobj)
    if not class_data.sys_params.types_cache.NSArray:
        class_data.sys_params.types_cache.NSSet = valobj.GetTarget().FindFirstType('NSSet').GetPointerType()

    # _productsRequestInternal (self->_productsRequestInternal)
    products_request_internal = valobj.GetChildMemberWithName("_productsRequestInternal")

    # _productIdentifiers (self->_internal->_productIdentifiers)
    product_identifiers = products_request_internal.CreateChildAtOffset("productIdentifiers",
                                                                        1 * class_data.sys_params.pointer_size,
                                                                        class_data.sys_params.types_cache.NSSet)
    product_identifiers_provider = NSSet.GetSummary_Impl(product_identifiers)

    if product_identifiers_provider.count == 1:
        product_identifiers_summary = "@\"{} product\"".format(product_identifiers_provider.count)
    else:
        product_identifiers_summary = "@\"{} products\"".format(product_identifiers_provider.count)

    # Summary
    return product_identifiers_summary


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKProductsRequest.SKProductsRequest_SummaryProvider \
                            --category StoreKit \
                            SKProductsRequest")
    debugger.HandleCommand("type category enable StoreKit")
