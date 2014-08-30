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


class SKProductsRequestInternal_SynthProvider(NSObject.NSObject_SynthProvider):
    # Class: SKProductsRequestInternal
    # Super class: NSObject
    # Name:                           armv7                 i386                  arm64                 x86_64
    # NSSet * _productIdentifiers   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKProductsRequestInternal_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKProductsRequestInternal"

        self.product_identifiers = None

    def get_product_identifiers(self):
        if self.product_identifiers:
            return self.product_identifiers

        self.product_identifiers = self.get_child_value("_productIdentifiers")
        return self.product_identifiers
