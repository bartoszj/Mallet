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
from ..CoreGraphics import CGImage
from .. import SummaryBase


class UIImageSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UIImage.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIImageSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIImage"

        self.register_child_value("image_ref", ivar_name="_imageRef",
                                  provider_class=CGImage.CGImageSyntheticProvider,
                                  summary_function=self.get_image_ref_summary)
        self.register_child_value("scale", ivar_name="_scale",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_scale_summary)

    @staticmethod
    def get_image_ref_summary(provider):
        """
        Returns CGImageRef summary.

        :param CGImage.CGImageSyntheticProvider provider: CGImageRef provider.
        :return: CGImageRef summary.
        """
        return provider.summary()

    @staticmethod
    def get_scale_summary(value):
        if value == 1:
            return None
        return "@{}x".format(SummaryBase.formatted_float(value))

    def get_size_summary(self):
        """
        Returns image size summary.

        :return: image size summary.
        :rtype str | None
        """
        scale = self.scale_value
        if scale == 0 or scale is None:
            return None

        width = self.image_ref_provider.width_value
        height = self.image_ref_provider.height_value
        if width is None or height is None:
            return None

        width = width / scale
        height = height / scale
        return "(width={}, height={})".format(SummaryBase.formatted_float(width), SummaryBase.formatted_float(height))

    def summary(self):
        summary = SummaryBase.join_summaries(self.get_size_summary(),
                                             self.scale_summary)
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIImageSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                           --category UIKit \
                           UIImage".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
