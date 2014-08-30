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
import CALayerInternalLayer


class CALayerIvars_SynthProvider(SummaryBase.SummaryBase_SynthProvider):
    # armv7, armv7, i386:
    # struct _CALayerIvars {
    #     int refcount;
    #     unsigned int magic;
    #     void *layer;
    #     void *unused1[8];
    # };
    #
    # arm64, x86_64:
    # struct _CALayerIvars {
    #     int refcount;
    #     unsigned int magic;
    #     void *layer;
    # };

    def __init__(self, value_obj, internal_dict):
        super(CALayerIvars_SynthProvider, self).__init__(value_obj, internal_dict)

        self.layer = None
        self.layer_provider = None

    def get_layer(self):
        if self.layer:
            return self.layer

        self.layer = self.get_child_value("layer")
        return self.layer

    def get_layer_provider(self):
        if self.layer_provider:
            return self.layer_provider

        layer = self.get_layer()
        self.layer_provider = CALayerInternalLayer.CALayerInternalLayer_SynthProvider(layer, self.internal_dict)
        return self.layer_provider