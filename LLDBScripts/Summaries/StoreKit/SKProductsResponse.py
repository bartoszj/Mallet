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
import SKProductsResponseInternal


class SKProductsResponse_SynthProvider(NSObject.NSObject_SynthProvider):
    # Class: SKProductsResponse
    # Super class: NSObject
    # Name:            armv7                 i386                  arm64                 x86_64
    # id _internal   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKProductsResponse_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProductsResponse"

        self.internal = None
        self.internal_provider = None

    @Helpers.save_parameter("internal")
    def get_internal(self):
        return self.get_child_value("_internal")

    @Helpers.save_parameter("internal_provider")
    def get_internal_provider(self):
        internal = self.get_internal()
        return None if internal is None else SKProductsResponseInternal.SKProductsResponseInternal_SynthProvider(internal, self.internal_dict)

    def get_products_value(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_products_value()

    def get_products_summary(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_products_summary()

    def get_invalid_identifiers_value(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_invalid_identifiers_value()

    def get_invalid_identifiers_summary(self):
        internal_provider = self.get_internal_provider()
        return None if internal_provider is None else internal_provider.get_invalid_identifiers_summary()

    def summary(self):
        products_value = self.get_products_value()
        products_summary = self.get_products_summary()

        invalid_identifiers_value = self.get_invalid_identifiers_value()
        invalid_identifiers_summary = self.get_invalid_identifiers_summary()

        summaries = []
        if products_value != 0:
            summaries.append(products_summary)
        if invalid_identifiers_value != 0:
            summaries.append(invalid_identifiers_summary)

        summary = None
        if len(summaries) > 0:
            summary = ", ".join(summaries)
        return "@\"{}\"".format(summary)


def SKProductsResponse_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, SKProductsResponse_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKProductsResponse.SKProductsResponse_SummaryProvider \
                            --category StoreKit \
                            SKProductsResponse")
    debugger.HandleCommand("type category enable StoreKit")
