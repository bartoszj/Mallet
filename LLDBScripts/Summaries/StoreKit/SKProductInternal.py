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


class SKProductInternal_SynthProvider(NSObject.NSObject_SynthProvider):
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

    def get_content_version(self):
        if self.content_version:
            return self.content_version

        self.content_version = self.get_child_value("_contentVersion")
        return self.content_version

    def get_downloadable(self):
        if self.downloadable:
            return self.downloadable

        self.downloadable = self.get_child_value("_downloadable")
        return self.downloadable

    def get_locale_identifier(self):
        if self.locale_identifier:
            return self.locale_identifier

        self.locale_identifier = self.get_child_value("_localeIdentifier")
        return self.locale_identifier

    def get_localized_description(self):
        if self.localized_description:
            return self.localized_description

        self.localized_description = self.get_child_value("_localizedDescription")
        return self.localized_description

    def get_localized_title(self):
        if self.localized_title:
            return self.localized_title

        self.localized_title = self.get_child_value("_localizedTitle")
        return self.localized_title

    def get_price(self):
        if self.price:
            return self.price

        self.price = self.get_child_value("_price")
        return self.price

    def get_product_identifier(self):
        if self.product_identifier:
            return self.product_identifier

        self.product_identifier = self.get_child_value("_productIdentifier")
        return self.product_identifier