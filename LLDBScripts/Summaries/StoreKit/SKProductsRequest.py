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

import summary_helpers
import SKRequest


class SKProductsRequest_SynthProvider(SKRequest.SKRequest_SynthProvider):
    # SKProductsRequest:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # SKRequestInternal *_requestInternal                                     4 = 0x04 / 4            8 = 0x08 / 8
    # SKProductsRequestInternal *_productsRequestInternal                     8 = 0x08 / 4           16 = 0x10 / 8

    # SKProductsRequestInternal:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSSet *_productIdentifiers                                             4 = 0x04 / 4             8 = 0x08 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKProductsRequest_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.products_request_internal = None
        self.product_identifiers = None
        self.product_identifiers_provider = None

        self.update()

    def update(self):
        # _productsRequestInternal (self->_productsRequestInternal)
        self.products_request_internal = self.value_obj.GetChildMemberWithName("_productsRequestInternal")
        #self.products_request_internal = self.value_obj.CreateChildAtOffset("_productsRequestInternal",
        #                                                                    2 * self.sys_params.pointer_size,
        #                                                                    self.sys_params.types_cache.id)
        self.product_identifiers = None
        self.product_identifiers_provider = None
        super(SKProductsRequest_SynthProvider, self).update()

    # _productIdentifiers (self->_internal->_productIdentifiers)
    def get_product_identifiers(self):
        if self.product_identifiers:
            return self.product_identifiers

        if self.products_request_internal:
            self.product_identifiers = self.products_request_internal.CreateChildAtOffset("productIdentifiers",
                                                                                          1 * self.sys_params.pointer_size,
                                                                                          self.sys_params.types_cache.NSSet)
        return self.product_identifiers

    def summary(self):
        identifiers = self.get_product_identifiers()
        identifiers_count = identifiers.GetNumChildren()

        if identifiers_count == 1:
            summary = "@\"{} product\"".format(identifiers_count)
        else:
            summary = "@\"{} products\"".format(identifiers_count)
        return summary


def SKProductsRequest_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, SKProductsRequest_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKProductsRequest.SKProductsRequest_SummaryProvider \
                            --category StoreKit \
                            SKProductsRequest")
    debugger.HandleCommand("type category enable StoreKit")
