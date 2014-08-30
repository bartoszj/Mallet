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

import Helpers
import NSObject
import SKProductInternal


class SKProduct_SynthProvider(NSObject.NSObject_SynthProvider):
    # Class: SKProduct
    # Super class: NSObject
    # Name:            armv7                 i386                  arm64                 x86_64
    # id _internal   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKProduct_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProduct"

        self.internal = None
        self.internal_provider = None

    def get_internal(self):
        if self.internal:
            return self.internal

        self.internal = self.get_child_value("_internal")
        return self.internal

    def get_internal_provider(self):
        if self.internal_provider:
            return self.internal_provider

        internal = self.get_internal()
        self.internal_provider = SKProductInternal.SKProductInternal_SynthProvider(internal, self.internal_dict)
        return self.internal_provider

    def summary(self):
        content_version_value = self.get_internal_provider().get_content_version().GetSummary()
        content_version_summary = None
        if content_version_value:
            content_version_summary = "version={}".format(content_version_value[2:-1])

        downloadable_value = self.get_internal_provider().get_downloadable().GetValueAsUnsigned()
        downloadable_summary = "downloadable={}".format("YES" if downloadable_value != 0 else "NO")

        # locale_identifier_value = self.get_internal_provider().get_locale_identifier().GetSummary()
        # locale_identifier_summary = None
        # if locale_identifier_value:
        #    locale_identifier_summary = "locale = {}".format(locale_identifier_value[2:-1])

        # localized_description_value = self.get_internal_provider().get_localized_description().GetSummary()
        # localized_description_summary = "description = {}".format(localized_description_value)

        localized_title_value = self.get_internal_provider().get_localized_title().GetSummary()
        localized_title_summary = localized_title_value

        price_value = self.get_internal_provider().get_price().GetSummary()
        price_summary = "price={}".format(price_value)

        # product_identifier_value = self.get_internal_provider().get_product_identifier().GetSummary()
        # product_identifier_summary = "productId = {}".format(product_identifier_value)

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
    return Helpers.generic_summary_provider(value_obj, internal_dict, SKProduct_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKProduct.SKProduct_SummaryProvider \
                            --category StoreKit \
                            SKProduct")
    debugger.HandleCommand("type category enable StoreKit")
