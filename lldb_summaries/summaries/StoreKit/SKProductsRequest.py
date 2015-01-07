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

from ...scripts import helpers
import SKRequest
import SKProductsRequestInternal


class SKProductsRequestSyntheticProvider(SKRequest.SKRequestSyntheticProvider):
    """
    Class representing SKProductsRequest.
    """
    def __init__(self, value_obj, internal_dict):
        super(SKProductsRequestSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProductsRequest"

        self.register_child_value("products_request_internal", ivar_name="_productsRequestInternal",
                                  provider_class=SKProductsRequestInternal.SKProductsRequestInternalSyntheticProvider,
                                  summary_function=self.get_products_request_internal_summary)

    @staticmethod
    def get_products_request_internal_summary(provider):
        """
        SKProductsRequestInternal summary.

        :param SKProductsRequestInternal.SKProductsRequestInternalSyntheticProvider provider: SKProductsRequestInternal provider.
        :return: SKProductsRequestInternal summary.
        :rtype: str
        """
        return provider.summary()

    def summary(self):
        return self.products_request_internal_summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, SKProductsRequestSyntheticProvider)


def lldb_init(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category StoreKit \
                            SKProductsRequest".format(__name__))
    debugger.HandleCommand("type category enable StoreKit")
