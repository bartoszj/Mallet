#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Bartosz Janda
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

import SummaryBase
import NSObject
import Helpers


class SKPaymentInternal_SynthProvider(NSObject.NSObjectSyntheticProvider):
    # Class: SKPaymentInternal
    # Super class: NSObject
    # Protocols: NSCopying
    # Name:                                        armv7                 i386                  arm64                 x86_64
    # NSString * _applicationUsername            4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # NSString * _partnerIdentifier              8 (0x008) / 4         8 (0x008) / 4        16 (0x010) / 8        16 (0x010) / 8
    # NSString * _partnerTransactionIdentifier  12 (0x00C) / 4        12 (0x00C) / 4        24 (0x018) / 8        24 (0x018) / 8
    # NSString * _productIdentifier             16 (0x010) / 4        16 (0x010) / 4        32 (0x020) / 8        32 (0x020) / 8
    # NSInteger _quantity                       20 (0x014) / 4        20 (0x014) / 4        40 (0x028) / 8        40 (0x028) / 8
    # NSData * _requestData                     24 (0x018) / 4        24 (0x018) / 4        48 (0x030) / 8        48 (0x030) / 8
    # NSDictionary * _requestParameters         28 (0x01C) / 4        28 (0x01C) / 4        56 (0x038) / 8        56 (0x038) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKPaymentInternal_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentInternal"

        self.application_username = None
        self.partner_identifier = None
        self.partner_transaction_identifier = None
        self.product_identifier = None
        self.quantity = None

    @Helpers.save_parameter("application_username")
    def get_application_username(self):
        return self.get_child_value("_applicationUsername")

    def get_application_username_value(self):
        return SummaryBase.get_stripped_summary_value(self.get_application_username())

    def get_application_username_summary(self):
        application_username_value = self.get_application_username_value()
        return None if application_username_value is None else "applicationUsername={}".format(application_username_value)

    @Helpers.save_parameter("partner_identifier")
    def get_partner_identifier(self):
        return self.get_child_value("_partnerIdentifier")

    @Helpers.save_parameter("partner_transaction_identifier")
    def get_partner_transaction_identifier(self):
        return self.get_child_value("_partnerTransactionIdentifier")

    @Helpers.save_parameter("product_identifier")
    def get_product_identifier(self):
        return self.get_child_value("_productIdentifier")

    def get_product_identifier_value(self):
        return SummaryBase.get_summary_value(self.get_product_identifier())

    def get_product_identifier_summary(self):
        product_identifier_value = self.get_product_identifier_value()
        return None if product_identifier_value is None else "{}".format(product_identifier_value)

    @Helpers.save_parameter("quantity")
    def get_quantity(self):
        return self.get_child_value("_quantity")

    def get_quantity_value(self):
        return SummaryBase.get_signed_value(self.get_quantity())

    def get_quantity_summary(self):
        quantity_value = self.get_quantity_value()
        return None if quantity_value is None else "quantity={}".format(quantity_value)
