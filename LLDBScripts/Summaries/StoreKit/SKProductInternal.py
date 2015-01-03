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

import NSObject
import Helpers


class SKProductInternal_SynthProvider(NSObject.NSObjectSyntheticProvider):
    # Class: SKProductInternal
    # Super class: NSObject
    # Name:                                 armv7                 i386                  arm64                 x86_64
    # NSString * _contentVersion          4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # BOOL _downloadable                  8 (0x008) / 1  + 3    8 (0x008) / 1  + 3   16 (0x010) / 1  + 7   16 (0x010) / 1  + 7
    # NSArray * _downloadContentLengths  12 (0x00C) / 4        12 (0x00C) / 4        24 (0x018) / 8        24 (0x018) / 8
    # NSString * _localeIdentifier       16 (0x010) / 4        16 (0x010) / 4        32 (0x020) / 8        32 (0x020) / 8
    # NSString * _localizedDescription   20 (0x014) / 4        20 (0x014) / 4        40 (0x028) / 8        40 (0x028) / 8
    # NSString * _localizedTitle         24 (0x018) / 4        24 (0x018) / 4        48 (0x030) / 8        48 (0x030) / 8
    # NSDecimalNumber * _price           28 (0x01C) / 4        28 (0x01C) / 4        56 (0x038) / 8        56 (0x038) / 8
    # NSLocale * _priceLocale            32 (0x020) / 4        32 (0x020) / 4        64 (0x040) / 8        64 (0x040) / 8
    # NSString * _productIdentifier      36 (0x024) / 4        36 (0x024) / 4        72 (0x048) / 8        72 (0x048) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKProductInternal_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProductInternal"

        self.content_version = None
        self.downloadable = None
        self.locale_identifier = None
        self.localized_description = None
        self.localized_title = None
        self.price = None
        self.product_identifier = None

    @Helpers.save_parameter("content_version")
    def get_content_version(self):
        return self.get_child_value("_contentVersion")

    def get_content_version_value(self):
        return self.get_stripped_summary_value(self.get_content_version())

    def get_content_version_summary(self):
        content_version_value = self.get_content_version_value()
        return None if content_version_value is None else "version={}".format(content_version_value)

    @Helpers.save_parameter("downloadable")
    def get_downloadable(self):
        return self.get_child_value("_downloadable")

    def get_downloadable_value(self):
        return self.get_unsigned_value(self.get_downloadable())

    def get_downloadable_summary(self):
        downloadable_value = self.get_downloadable_value()
        return None if downloadable_value is None else "downloadable={}".format("YES" if downloadable_value != 0 else "NO")

    @Helpers.save_parameter("locale_identifier")
    def get_locale_identifier(self):
        return self.get_child_value("_localeIdentifier")

    @Helpers.save_parameter("localized_description")
    def get_localized_description(self):
        return self.get_child_value("_localizedDescription")

    @Helpers.save_parameter("localized_title")
    def get_localized_title(self):
        return self.get_child_value("_localizedTitle")

    def get_localized_title_value(self):
        return self.get_summary_value(self.localized_title())

    def get_localized_title_summary(self):
        localized_title_value = self.get_localized_title_value()
        return None if localized_title_value is None else "{}".format(localized_title_value)

    @Helpers.save_parameter("price")
    def get_price(self):
        return self.get_child_value("_price")

    def get_price_value(self):
        return self.get_summary_value(self.get_price())

    def get_price_summary(self):
        price_value = self.get_price_value()
        return None if price_value is None else "price={}".format(price_value)

    @Helpers.save_parameter("product_identifier")
    def get_product_identifier(self):
        return self.get_child_value("_productIdentifier")
