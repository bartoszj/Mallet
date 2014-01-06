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
import summary_helpers
import NSObject


class SKPayment_SynthProvider(NSObject.NSObject_SynthProvider):
    # SKPayment:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # SKPaymentInternal *_internal                                            4 = 0x04 / 4            4 = 0x08 / 8

    # SKPaymentInternal:
    # Offset / size                                                         32bit:                  64bit:
    #
    # NSString *_applicationUsername                                          4 = 0x04 / 4            8 = 0x08 / 8
    # NSString *_productIdentifier                                            8 = 0x08 / 4           16 = 0x10 / 8
    # NSInteger _quantity                                                    12 = 0x0c / 4           24 = 0x18 / 8
    # NSData *_requestData                                                   16 = 0x10 / 4           32 = 0x20 / 8
    # NSDictionary *_requestParameters                                       20 = 0x14 / 4           40 = 0x28 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKPayment_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.internal = None
        self.application_username = None
        self.product_identifier = None
        self.quantity = None

        self.update()

    def update(self):
        self.internal = self.value_obj.GetChildMemberWithName("_internal")
        self.application_username = None
        self.product_identifier = None
        self.quantity = None
        super(SKPayment_SynthProvider, self).update()

    # _applicationUsername (self->_internal->_applicationUsername)
    def get_application_username(self):
        if self.application_username:
            return self.application_username

        if self.internal:
            self.application_username = self.internal.CreateChildAtOffset("applicationUsername",
                                                                          1 * self.sys_params.pointer_size,
                                                                          self.sys_params.types_cache.NSString)
        return self.application_username

    # _productIdentifier (self->_internal->_productIdentifier)
    def get_product_identifier(self):
        if self.product_identifier:
            return self.product_identifier

        if self.internal:
            self.product_identifier = self.internal.CreateChildAtOffset("productIdentifier",
                                                                        2 * self.sys_params.pointer_size,
                                                                        self.sys_params.types_cache.NSString)
        return self.product_identifier

    # _quantity (self->_internal->_quantity)
    def get_quantity(self):
        if self.quantity:
            return self.quantity

        if self.internal:
            self.quantity = self.internal.CreateChildAtOffset("quantity",
                                                              3 * self.sys_params.pointer_size,
                                                              self.sys_params.types_cache.int)
        return self.quantity

    def summary(self):
        application_username_value = self.get_application_username().GetSummary()
        application_username_summary = None
        if application_username_value:
            application_username_summary = "applicationUsername={}".format(application_username_value[2:-1])

        product_identifier_value = self.get_product_identifier().GetSummary()
        product_identifier_summary = product_identifier_value

        quantity_value = self.get_quantity().GetValueAsSigned()
        quantity_summary = "quantity={}".format(quantity_value)

        # Summaries
        summaries = [product_identifier_summary]
        if application_username_value:
            summaries.append(application_username_summary)
        if quantity_value != 1:
            summaries.append(quantity_summary)

        summary = ", ".join(summaries)
        return summary


def SKPayment_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, SKPayment_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKPayment.SKPayment_SummaryProvider \
                            --category StoreKit \
                            SKPayment SKMutablePayment")
    debugger.HandleCommand("type category enable StoreKit")
