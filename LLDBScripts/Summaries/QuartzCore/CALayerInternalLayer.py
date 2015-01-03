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
import CADoublePoint
import CADoubleRect
import Helpers


class CALayerInternalLayer_SynthProvider(SummaryBase.SummaryBaseSyntheticProvider):
    # Name:                          armv7                 i386                  arm64                 x86_64
    # CADoublPoint position       32 (0x020) / 16       32 (0x020) / 16       48 (0x030) / 16       48 (0x030) / 16
    # CADoubleRect bounds         48 (0x030) / 32       48 (0x030) / 32       64 (0x040) / 16       64 (0x040) / 16

    def __init__(self, value_obj, internal_dict):
        super(CALayerInternalLayer_SynthProvider, self).__init__(value_obj, internal_dict)

        self.position = None
        self.position_provider = None
        self.bounds = None
        self.bounds_provider = None

    @Helpers.save_parameter("position")
    def get_position(self):
        if self.is_64bit:
            offset = 0x30
        else:
            offset = 0x20

        # Using CGPoint for workaround. LLDB cannot find type CADoublePoint.
        return self.get_child_value("position", type_name="CGPoint", offset=offset)

    @Helpers.save_parameter("position_provider")
    def get_position_provider(self):
        position = self.get_position()
        return None if position is None else CADoublePoint.CADoublePoint_SynthProvider(position, self.internal_dict)

    @Helpers.save_parameter("bounds")
    def get_bounds(self):
        if self.is_64bit:
            offset = 0x40
        else:
            offset = 0x30

        # Using CGRect for workaround. LLDB cannot find type CADoubleRect.
        return self.get_child_value("bounds", type_name="CGRect", offset=offset)

    @Helpers.save_parameter("bounds_provider")
    def get_bounds_provider(self):
        bounds = self.get_bounds()
        return None if bounds is None else CADoubleRect.CADoubleRect_SynthProvider(bounds, self.internal_dict)
