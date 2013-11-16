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
import objc_runtime
import summary_helpers

statistics = lldb.formatters.metrics.Metrics()
statistics.add_metric('invalid_isa')
statistics.add_metric('invalid_pointer')
statistics.add_metric('unknown_class')
statistics.add_metric('code_notrun')


class SKProduct_SynthProvider(object):
    # SKProduct:
    # Offset / size                                 32bit:              64bit:
    #
    # Class isa                                      0 = 0x00 / 4        0 = 0x00 / 8
    # SKProductInternal *_internal                   4 = 0x04 / 4        8 = 0x08 / 8

    # SKProductInternal:
    # Offset / size                                 32bit:              64bit:
    #
    # Class isa                                      0 = 0x00 / 4        0 = 0x00 / 8
    # NSString *_contentVersion                      4 = 0x04 / 4        8 = 0x08 / 8
    # BOOL _downloadable                             8 = 0x08 / 1 + 3   16 = 0x10 / 1 + 7
    # NSArray *_downloadContentLengths              12 = 0x0c / 4       24 = 0x18 / 8
    # NSString *_localeIdentifier                   16 = 0x10 / 4       32 = 0x20 / 8
    # NSString *_localizedDescription               20 = 0x14 / 4       40 = 0x28 / 8
    # NSString *_localizedTitle                     24 = 0x18 / 4       48 = 0x30 / 8
    # NSDecimalNumber *_price                       28 = 0x1c / 4       56 = 0x38 / 8
    # NSLocale *_priceLocale                        32 = 0x20 / 4       64 = 0x40 / 8
    # NSString *_productIdentifier                  36 = 0x24 / 4       72 = 0x48 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKProduct_SynthProvider, self).__init__()
        self.value_obj = value_obj
        self.sys_params = sys_params
        self.internal_dict = internal_dict

        self.internal = None
        self.content_version = None
        self.downloadable = None
        self.locale_identifier = None
        self.localized_description = None
        self.localized_title = None
        self.price = None
        self.product_identifier = None
        self.update()

    def update(self):
        self.adjust_for_architecture()
        # _internal (self->_internal)
        self.internal = self.value_obj.GetChildMemberWithName("_internal")
        self.content_version = None
        self.downloadable = None
        self.locale_identifier = None
        self.localized_description = None
        self.localized_title = None
        self.product_identifier = None
        self.price = None

    def adjust_for_architecture(self):
        pass

    # _contentVersion (self->_internal->_contentVersion)
    def get_content_version(self):
        if self.content_version:
            return self.content_version

        if self.internal:
            self.content_version = self.internal.CreateChildAtOffset("contentVersion",
                                                                     1 * self.sys_params.pointer_size,
                                                                     self.sys_params.types_cache.NSString)
        return self.content_version

    # _downloadable (self->_internal->_downloadable)
    def get_downloadable(self):
        if self.downloadable:
            return self.downloadable

        if self.internal:
            self.downloadable = self.internal.CreateChildAtOffset("downloadable",
                                                                  2 * self.sys_params.pointer_size,
                                                                  self.sys_params.types_cache.char)
        return self.downloadable

    # _localeIdentifier (self->_internal->_localeIdentifier)
    def get_locale_identifier(self):
        if self.locale_identifier:
            return self.locale_identifier

        if self.internal:
            self.locale_identifier = self.internal.CreateChildAtOffset("localeIdentifier",
                                                                       4 * self.sys_params.pointer_size,
                                                                       self.sys_params.types_cache.NSString)
        return self.locale_identifier

    # _localizedDescription (self->_internal->_localizedDescription)
    def get_localized_description(self):
        if self.localized_description:
            return self.localized_description

        if self.internal:
            self.localized_description = self.internal.CreateChildAtOffset("localizedDescription",
                                                                           5 * self.sys_params.pointer_size,
                                                                           self.sys_params.types_cache.NSString)
        return self.localized_description

    # _localizedTitle (self->_internal->_localizedTitle)
    def get_localized_title(self):
        if self.localized_title:
            return self.localized_title

        if self.internal:
            self.localized_title = self.internal.CreateChildAtOffset("localizedTitle",
                                                                     6 * self.sys_params.pointer_size,
                                                                     self.sys_params.types_cache.NSString)
        return self.localized_title

    # _price (self->internal->_price)
    def get_price(self):
        if self.price:
            return self.price

        if self.internal:
            self.price = self.internal.CreateChildAtOffset("price",
                                                           7 * self.sys_params.pointer_size,
                                                           self.sys_params.types_cache.NSDecimalNumber)
        return self.price

    # _productIdentifier (self->_internal->_productIdentifier)
    def get_product_identifier(self):
        if self.product_identifier:
            return self.product_identifier

        if self.internal:
            self.product_identifier = self.internal.CreateChildAtOffset("productIdentifier",
                                                                        9 * self.sys_params.pointer_size,
                                                                        self.sys_params.types_cache.NSString)
        return self.product_identifier

    def summary(self):
        content_version_value = self.get_content_version().GetSummary()
        content_version_summary = None
        if content_version_value:
            content_version_summary = "version = {}".format(content_version_value[2:-1])

        downloadable_value = self.get_downloadable().GetValueAsUnsigned()
        downloadable_summary = "downloadable = {}".format("YES" if downloadable_value != 0 else "NO")

        #locale_identifier_value = self.get_locale_identifier().GetSummary()
        #locale_identifier_summary = None
        #if locale_identifier_value:
        #    locale_identifier_summary = "locale = {}".format(locale_identifier_value[2:-1])

        #localized_description_value = self.get_localized_description().GetSummary()
        #localized_description_summary = "description = {}".format(localized_description_value)

        localized_title_value = self.get_localized_title().GetSummary()
        localized_title_summary = localized_title_value

        price_value = self.get_price().GetSummary()
        price_summary = "price = {}".format(price_value)

        #product_identifier_value = self.get_product_identifier().GetSummary()
        #product_identifier_summary = "productId = {}".format(product_identifier_value)

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


def SKProduct_SummaryProvider(value_obj, internal_dict):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    summary_helpers.update_sys_params(value_obj, class_data.sys_params)
    if wrapper is not None:
        return wrapper.message()

    wrapper = SKProduct_SynthProvider(value_obj, class_data.sys_params, internal_dict)
    if wrapper is not None:
        return wrapper.summary()
    return "Summary Unavailable"


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKProduct.SKProduct_SummaryProvider \
                            --category StoreKit \
                            SKProduct")
    debugger.HandleCommand("type category enable StoreKit")
