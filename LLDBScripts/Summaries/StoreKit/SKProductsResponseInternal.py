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


class SKProductsResponseInternal_SynthProvider(NSObject.NSObject_SynthProvider):
    # Class: SKProductsResponseInternal
    # Super class: NSObject
    # Name:                             armv7                 i386                  arm64                 x86_64
    # NSArray * _invalidIdentifiers   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # NSArray * _products             8 (0x008) / 4         8 (0x008) / 4        16 (0x010) / 8        16 (0x010) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKProductsResponseInternal_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProductsResponseInternal"

        self.products = None
        self.invalid_identifiers = None

    def get_products(self):
        if self.products:
            return self.products

        self.products = self.get_child_value("_products")
        return self.products

    def get_invalid_identifiers(self):
        if self.invalid_identifiers:
            return self.invalid_identifiers

        self.invalid_identifiers = self.get_child_value("_invalidIdentifiers")
        return self.invalid_identifiers
