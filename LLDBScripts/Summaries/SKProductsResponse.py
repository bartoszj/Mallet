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
import CFArray
import objc_runtime
import summary_helpers

statistics = lldb.formatters.metrics.Metrics()
statistics.add_metric('invalid_isa')
statistics.add_metric('invalid_pointer')
statistics.add_metric('unknown_class')
statistics.add_metric('code_notrun')


class SKProductsResponse_SynthProvider(object):
    # SKProductsResponse:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # Class isa                                                               0 = 0x00 / 4            0 = 0x00 / 8
    # SKProductsResponseInternal *_internal                                   4 = 0x04 / 4            8 = 0x08 / 8

    # SKProductsResponseInternal:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # Class isa                                                               0 = 0x00 / 4            0 = 0x00 / 8
    # NSArray *_invalidIdentifiers                                            4 = 0x04 / 4            8 = 0x08 / 8
    # NSArray *_products                                                      8 = 0x08 / 4           16 = 0x10 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKProductsResponse_SynthProvider, self).__init__()
        self.value_obj = value_obj
        self.sys_params = sys_params
        self.internal_dict = internal_dict
        self.internal = None
        self.invalid_identifiers = None
        self.invalid_identifiers_provider = None
        self.products = None
        self.products_provider = None
        self.update()

    def update(self):
        self.adjust_for_architecture()
        # _internal (self->_internal)
        self.internal = self.value_obj.GetChildMemberWithName("_internal")
        self.invalid_identifiers = None
        self.invalid_identifiers_provider = None
        self.products = None
        self.products_provider = None

    def adjust_for_architecture(self):
        pass

    # _invalidIdentifiers (self->_internal->_invalidIdentifiers)
    def get_invalid_identifiers(self):
        if self.invalid_identifiers:
            return self.invalid_identifiers

        if self.internal:
            self.invalid_identifiers = self.internal.CreateChildAtOffset("invalidIdentifiers",
                                                                         1 * self.sys_params.pointer_size,
                                                                         self.sys_params.types_cache.NSArray)
        return self.invalid_identifiers

    # NSArray provider
    def get_invalid_identifiers_provider(self):
        if self.invalid_identifiers_provider:
            self.invalid_identifiers_provider

        if self.get_invalid_identifiers():
            self.invalid_identifiers_provider = CFArray.NSArray_SynthProvider(self.get_invalid_identifiers(),
                                                                              self.internal_dict)
        return self.invalid_identifiers_provider

    # _products (self->_internal->_products)
    def get_products(self):
        if self.products:
            return self.products

        if self.internal:
            self.products = self.internal.CreateChildAtOffset("products",
                                                              2 * self.sys_params.pointer_size,
                                                              self.sys_params.types_cache.NSArray)
        return self.products

    # NSArray provider
    def get_products_provider(self):
        if self.products_provider:
            self.products_provider

        if self.get_products():
            self.products_provider = CFArray.NSArray_SynthProvider(self.get_products(), self.internal_dict)
        return self.products_provider

    def summary(self):
        invalid_identifiers_count = self.get_invalid_identifiers_provider().num_children()
        invalid_identifiers_summary = "{} invalid".format(invalid_identifiers_count)
        products_count = self.get_products_provider().num_children()
        products_summary = "{} valid".format(products_count)

        summaries = []
        if products_count != 0:
            summaries.append(products_summary)
        if invalid_identifiers_count != 0:
            summaries.append(invalid_identifiers_summary)

        summary = None
        if len(summaries) > 0:
            summary = ", ".join(summaries)
        return "@\"{}\"".format(summary)


def SKProductsResponse_SummaryProvider(value_obj, internal_dict):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    summary_helpers.update_sys_params(value_obj, class_data.sys_params)
    if wrapper is not None:
        return wrapper.message()

    wrapper = SKProductsResponse_SynthProvider(value_obj, class_data.sys_params, internal_dict)
    if wrapper is not None:
        return wrapper.summary()
    return "Summary Unavailable"


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKProductsResponse.SKProductsResponse_SummaryProvider \
                            --category StoreKit \
                            SKProductsResponse")
    debugger.HandleCommand("type category enable StoreKit")
