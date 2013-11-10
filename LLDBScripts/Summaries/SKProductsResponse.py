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


def SKProductsResponse_SummaryProvider(valobj, dict):

    # Class data
    class_data, wrapper = get_class_data(valobj)
    if not class_data.sys_params.types_cache.NSArray:
        class_data.sys_params.types_cache.NSArray = valobj.GetTarget().FindFirstType('NSArray').GetPointerType()
    if not class_data.sys_params.types_cache.NSUInteger:
        if class_data.sys_params.is_64_bit:
            class_data.sys_params.types_cache.NSUInteger = valobj.GetType().GetBasicType(lldb.eBasicTypeUnsignedLong)
        else:
            class_data.sys_params.types_cache.NSUInteger = valobj.GetType().GetBasicType(lldb.eBasicTypeUnsignedInt)

    # _internal (self->_internal)
    internal = valobj.GetChildMemberWithName("_internal")

    # _invalidIdentifiers (self->_internal->_invalidIdentifiers)
    invalid_identifiers = internal.CreateChildAtOffset("invalidIdentifiers",
                                                       1 * class_data.sys_params.pointer_size,
                                                       class_data.sys_params.types_cache.NSArray)
    # type: __NSCFArray
    invalid_identifiers_count_vo = invalid_identifiers.CreateChildAtOffset("count",
                                                                           class_data.sys_params.cfruntime_size,
                                                                           class_data.sys_params.types_cache.NSUInteger)
    invalid_identifiers_count = invalid_identifiers_count_vo.GetValueAsUnsigned()
    invalid_identifiers_summary = "{} invalids".format(invalid_identifiers_count)

    # _products (self->_internal->_products)
    products = internal.CreateChildAtOffset("products",
                                            2 * class_data.sys_params.pointer_size,
                                            class_data.sys_params.types_cache.NSArray)
    # type: __NSArrayI
    products_count_vo = products.CreateChildAtOffset("count",
                                                     class_data.sys_params.pointer_size,
                                                     class_data.sys_params.types_cache.NSUInteger)
    products_count = products_count_vo.GetValueAsUnsigned()
    products_summary = "{} valids".format(products_count)

    # Summaries
    summaries = []
    if products_count != 0:
        summaries.append(products_summary)
    if invalid_identifiers_count != 0:
        summaries.append(invalid_identifiers_summary)

    summary = None
    if len(summaries) > 0:
        summary = ", ".join(summaries);
    return "@\"{}\"".format(summary)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKProductsResponse.SKProductsResponse_SummaryProvider \
                            --category StoreKit \
                            SKProductsResponse")
    debugger.HandleCommand("type category enable StoreKit")
