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


def SKProduct_SummaryProvider(valobj, dict):

    # Class data
    class_data, wrapper = get_class_data(valobj)
    if not class_data.sys_params.types_cache.NSString:
        class_data.sys_params.types_cache.NSString = valobj.GetTarget().FindFirstType('NSString').GetPointerType()
    if not class_data.sys_params.types_cache.NSDecimalNumber:
        class_data.sys_params.types_cache.NSDecimalNumber = valobj.GetTarget().FindFirstType('NSDecimalNumber').GetPointerType()
    if not(class_data.sys_params.types_cache.char):
        class_data.sys_params.types_cache.char = valobj.GetType().GetBasicType(lldb.eBasicTypeChar)

    # _internal (self->_internal)
    internal = valobj.GetChildMemberWithName("_internal")

    # _contentVersion (self->_internal->_contentVersion)
    content_version = internal.CreateChildAtOffset("contentVersion",
                                                   1 * class_data.sys_params.pointer_size,
                                                   class_data.sys_params.types_cache.NSString)
    content_version_value = content_version.GetSummary()
    content_version_summary = None
    if content_version_value:
        content_version_summary = "version = {}".format(content_version_value[2:-1])

    # _downloadable (self->_internal->_downloadable)
    downloadable = internal.CreateChildAtOffset("downloadable",
                                                2 * class_data.sys_params.pointer_size,
                                                class_data.sys_params.types_cache.char)
    downloadable_value = downloadable.GetValueAsUnsigned()
    downloadable_summary = "downloadable = {}".format("YES" if downloadable_value != 0 else "NO")

    # _localeIdentifier (self->_internal->_localeIdentifier)
    locale_identifier = internal.CreateChildAtOffset("localeIdentifier",
                                                     4 * class_data.sys_params.pointer_size,
                                                     class_data.sys_params.types_cache.NSString)
    locale_identifier_value = locale_identifier.GetSummary()
    locale_identifier_summary = None
    if locale_identifier_value:
        locale_identifier_summary = "locale = {}".format(locale_identifier_value[2:-1])

    # _localizedDescription (self->_internal->_localizedDescription)
    localized_description = internal.CreateChildAtOffset("localizedDescription",
                                                         5 * class_data.sys_params.pointer_size,
                                                         class_data.sys_params.types_cache.NSString)
    localized_description_value = localized_description.GetSummary()
    localized_description_summary = "description = {}".format(localized_description_value)

    # _localizedTitle (self->_internal->_localizedTitle)
    localized_title = internal.CreateChildAtOffset("localizedTitle",
                                                   6 * class_data.sys_params.pointer_size,
                                                   class_data.sys_params.types_cache.NSString)
    localized_title_value = localized_title.GetSummary()
    localized_title_summary = localized_title_value

    # _price (self->internal->_price)
    price = internal.CreateChildAtOffset("price",
                                         7 * class_data.sys_params.pointer_size,
                                         class_data.sys_params.types_cache.NSDecimalNumber)
    price_value = price.GetSummary()
    price_summary = "price = {}".format(price_value)

    # _productIdentifier (self->_internal->_productIdentifier)
    product_identifier = internal.CreateChildAtOffset("productIdentifier",
                                                      9 * class_data.sys_params.pointer_size,
                                                      class_data.sys_params.types_cache.NSString)
    product_identifier_value = product_identifier.GetSummary()
    product_identifier_summary = "productId = {}".format(product_identifier_value)

    # Summaries
    summaries = []
    if localized_title_value:
        summaries.append(localized_title_summary)
    if price_value:
        summaries.append(price_summary)
    if downloadable_value != 0:
        summaries.append(downloadable_summary)
        summaries.append(content_version_summary)

    summary = ", ".join(summaries)
    return summary


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F SKProduct.SKProduct_SummaryProvider \
                            --category StoreKit \
                            SKProduct")
    debugger.HandleCommand("type category enable StoreKit")
