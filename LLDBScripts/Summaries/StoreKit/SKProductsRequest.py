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
import SKRequest
import SKProductsRequestInternal


class SKProductsRequest_SynthProvider(SKRequest.SKRequest_SynthProvider):
    # Class: SKProductsRequest
    # Super class: SKRequest
    # Name:                           armv7                 i386                  arm64                 x86_64
    # id _productsRequestInternal   8 (0x008) / 4         8 (0x008) / 4        16 (0x010) / 8        16 (0x010) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKProductsRequest_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProductsRequest"

        self.products_request_internal = None
        self.products_request_internal_provider = None

    def get_products_request_internal(self):
        if self.products_request_internal:
            return self.products_request_internal

        self.products_request_internal = self.get_child_value("_productsRequestInternal")
        return self.products_request_internal

    def get_products_request_internal_provider(self):
        if self.products_request_internal_provider:
            return self.products_request_internal_provider

        products_request_internal = self.get_products_request_internal()
        self.products_request_internal_provider = SKProductsRequestInternal.SKProductsRequestInternal_SynthProvider(products_request_internal, self.internal_dict)
        return self.products_request_internal_provider

    def summary(self):
        product_identifiers = self.get_products_request_internal_provider().get_product_identifiers()
        product_identifiers_count = product_identifiers.GetNumChildren()

        if product_identifiers_count == 1:
            summary = "@\"{} product\"".format(product_identifiers_count)
        else:
            summary = "@\"{} products\"".format(product_identifiers_count)
        return summary


def SKProductsRequest_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, SKProductsRequest_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKProductsRequest.SKProductsRequest_SummaryProvider \
                            --category StoreKit \
                            SKProductsRequest")
    debugger.HandleCommand("type category enable StoreKit")
