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


import SummaryBase
import CGPoint
import CGSize


class CGRect_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # struct CGRect {
    #   CGPoint origin;
    #   CGSize size;
    # };
    # typedef struct CGRect CGRect;
    def __init__(self, value_obj, internal_dict):
        super(CGRect_SynthProvider, self).__init__(value_obj, internal_dict)

        self.origin = None
        self.size = None

        self.origin_provider = None
        self.size_provider = None

    def get_origin(self):
        if self.origin:
            return self.origin

        self.origin = self.get_child_value("origin")
        return self.origin

    def get_origin_provider(self):
        if self.origin_provider:
            return self.origin_provider

        origin = self.get_origin()
        if origin is None:
            return None

        self.origin_provider = CGPoint.CGPoint_SynthProvider(origin, self.internal_dict)
        return self.origin_provider

    def get_size(self):
        if self.size:
            return self.size

        self.size = self.get_child_value("size")
        return self.size

    def get_size_provider(self):
        if self.size_provider:
            return self.size_provider

        size = self.get_size()
        if size is None:
            return None

        self.size_provider = CGSize.CGSize_SynthProvider(size, self.internal_dict)
        return self.size_provider
