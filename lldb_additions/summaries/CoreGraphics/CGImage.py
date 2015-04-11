#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Bartosz Janda
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

from ...scripts import helpers
from ..Foundation import NSObject
from .. import SummaryBase


class CGImageSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing CGImage.

    :param int width_offset: Offset to image width.
    :param int height_offset: Offset to image height.
    """
    # CGImage:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSInteger width                                                      12 = 0x0c / 4           24 = 0x18 / 8
    # NSInteger height                                                     16 = 0x10 / 4           32 = 0x20 / 8

    def __init__(self, value_obj, internal_dict):
        super(CGImageSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            self.width_offset = 0x18
            self.height_offset = 0x20
        else:
            self.width_offset = 0x0c
            self.height_offset = 0x10

        self.register_child_value("width", type_name="NSInteger", offset=self.width_offset,
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_width_summary)
        self.register_child_value("height", type_name="NSInteger", offset=self.height_offset,
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_height_summary)

    @staticmethod
    def get_width_summary(value):
        return "width={}".format(value)

    @staticmethod
    def get_height_summary(value):
        return "height={}".format(value)

    def get_size_summary(self):
        return "({}, {})".format(self.width_summary, self.height_summary)

    def summary(self):
        return self.get_size_summary()


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, CGImageSyntheticProvider)
