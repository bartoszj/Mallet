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

from ..common import SummaryBase
from ..Foundation import NSObject


class SKPaymentInternalSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing SKPaymentInternal.
    """
    def __init__(self, value_obj, internal_dict):
        super(SKPaymentInternalSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKPaymentInternal"

        self.register_child_value("application_username", ivar_name="_applicationUsername",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_application_username_summary)
        self.register_child_value("partner_identifier", ivar_name="_partnerIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_partner_identifier_summary)
        self.register_child_value("partner_transaction_identifier", ivar_name="_partnerTransactionIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_partner_transaction_identifier_summary)
        self.register_child_value("product_identifier", ivar_name="_productIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_product_identifier_summary)
        self.register_child_value("quantity", ivar_name="_quantity",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_quantity_summary)

    @staticmethod
    def get_application_username_summary(value):
        return "applicationUsername={}".format(value)

    @staticmethod
    def get_partner_identifier_summary(value):
        return "partnerIdentifier={}".format(value)

    @staticmethod
    def get_partner_transaction_identifier_summary(value):
        return "partnerTransactionIdentifier={}".format(value)

    @staticmethod
    def get_product_identifier_summary(value):
        return "{}".format(value)

    @staticmethod
    def get_quantity_summary(value):
        if value != 1:
            return "quantity={}".format(value)
        return None

    def summaries_parts(self):
        return [self.product_identifier_summary, self.quantity_summary,
                self.application_username_summary]
