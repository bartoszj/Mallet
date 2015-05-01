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
import CADoublePoint
import CADoubleRect


class CALayerInternalLayerSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing CALayer internals.
    """
    # Name:                          armv7                 i386                  arm64                 x86_64
    # CADoublPoint position       32 (0x020) / 16       32 (0x020) / 16       48 (0x030) / 16       48 (0x030) / 16
    # CADoubleRect bounds         48 (0x030) / 32       48 (0x030) / 32       64 (0x040) / 16       64 (0x040) / 16

    def __init__(self, value_obj, internal_dict):
        super(CALayerInternalLayerSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            position_offset = 0x30
            bounds_offset = 0x40
        else:
            position_offset = 0x20
            bounds_offset = 0x30

        # Using CGPoint for workaround. LLDB cannot find type CADoublePoint.
        self.register_child_value("position", ivar_name="position", type_name="CGPoint", offset=position_offset,
                                  provider_class=CADoublePoint.CADoublePointSyntheticProvider,
                                  summary_function=self.get_position_summary)
        # Using CGRect for workaround. LLDB cannot find type CADoubleRect.
        self.register_child_value("bounds", ivar_name="bounds", type_name="CGRect", offset=bounds_offset,
                                  provider_class=CADoubleRect.CADoubleRectSyntheticProvider,
                                  summary_function=self.get_bounds_summary)

    @staticmethod
    def get_position_summary(provider):
        """
        Returns position summary.

        :param CADoublePoint.CADoublePointSyntheticProvider provider: Position provider.
        :return: Position summary.
        :rtype: str
        """
        return "position=({}, {})".format(SummaryBase.formatted_float(provider.x_value),
                                          SummaryBase.formatted_float(provider.y_value))

    @staticmethod
    def get_bounds_summary(provider):
        """
        Returns bounds summary.

        :param CADoubleRect.CADoubleRectSyntheticProvider provider: Bounds provider.
        :return: Bounds summary.
        :rtype: str
        """
        return "bounds=({} {}; {} {})".format(SummaryBase.formatted_float(provider.origin_provider.x_value),
                                              SummaryBase.formatted_float(provider.origin_provider.y_value),
                                              SummaryBase.formatted_float(provider.size_provider.width_value),
                                              SummaryBase.formatted_float(provider.size_provider.height_value))

    def summaries_parts(self):
        return [self.position_summary, self.bounds_summary]
