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


class SKRequestInternal_SynthProvider(NSObject.NSObjectSyntheticProvider):
    # Class: SKRequestInternal
    # Super class: NSObject
    # Name:                                   armv7                 i386                  arm64                 x86_64
    # NSInteger _backgroundTaskIdentifier   4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # SKPaymentQueueClient * _client        8 (0x008) / 4         8 (0x008) / 4        16 (0x010) / 8        16 (0x010) / 8
    # SKXPCConnection * _connection        12 (0x00C) / 4        12 (0x00C) / 4        24 (0x018) / 8        24 (0x018) / 8
    # id <SKRequestDelegate> _delegate     16 (0x010) / 4        16 (0x010) / 4        32 (0x020) / 8        32 (0x020) / 8
    # int _state                           20 (0x014) / 4        20 (0x014) / 4        40 (0x028) / 4        40 (0x028) / 4

    def __init__(self, value_obj, internal_dict):
        super(SKRequestInternal_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKRequestInternal"
