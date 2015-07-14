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

from .. import SummaryBase
from ..Foundation import NSObject


class SKProductInternalSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing SKProductInternal.
    """
    def __init__(self, value_obj, internal_dict):
        super(SKProductInternalSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProductInternal"

        self.register_child_value("content_version", ivar_name="_contentVersion",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_content_version_summary)
        self.register_child_value("downloadable", ivar_name="_downloadable",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_downloadable_summary)
        self.register_child_value("locale_identifier", ivar_name="_localeIdentifier",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_locale_identifier_summary)
        self.register_child_value("localized_description", ivar_name="_localizedDescription",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_localized_description_summary)
        self.register_child_value("localized_title", ivar_name="_localizedTitle",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_localized_title_summary)
        self.register_child_value("price", ivar_name="_price",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_price_summary)
        self.register_child_value("product_identifier", ivar_name="_productIdentifier",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_price_summary)

    @staticmethod
    def get_content_version_summary(value):
        return "version={}".format(value)

    @staticmethod
    def get_downloadable_summary(value):
        if value is True:
            return "downloadable=YES"
        return None

    @staticmethod
    def get_locale_identifier_summary(value):
        return "localeIdentifier={}".format(value)

    @staticmethod
    def get_localized_description_summary(value):
        return "description={}".format(value)

    @staticmethod
    def get_localized_title_summary(value):
        return "{}".format(value)

    @staticmethod
    def get_price_summary(value):
        return "price={}".format(value)

    @staticmethod
    def get_product_identifier_summary(value):
        return "identifier={}".format(value)

    def summaries_parts(self):
        return [self.localized_title_summary, self.price_summary,
                self.downloadable_summary, self.content_version_summary]
