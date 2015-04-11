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

from ...scripts import helpers
from ..Foundation import NSObject
import CALayerIvars


class CALayerSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing CALayer.
    """
    def __init__(self, value_obj, internal_dict):
        super(CALayerSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "CALayer"

        self.register_child_value("attr", ivar_name="_attr",
                                  provider_class=CALayerIvars.CALayerIvarsSyntheticProvider,
                                  summary_function=self.get_attr_summary)

    @staticmethod
    def get_attr_summary(provider):
        """
        Returns attr provider.

        :param CALayerIvars.CALayerIvarsSyntheticProvider provider: Attributes provider.
        :return: Attributes summary.
        :rtype: str
        """
        return provider.summary()

    def get_position_provider(self):
        """
        Returns position provider.

        :return: Position provider.
        :rtype: CADoublePoint.CADoublePointSyntheticProvider
        """
        return self.attr_provider.layer_provider.position_provider

    def get_bounds_provider(self):
        """
        Returns bounds provider.

        :return: bounds provider.
        :rtype: CADoubleRect.CADoubleRectSyntheticProvider
        """
        return self.attr_provider.layer_provider.bounds_provider

    def summary(self):
        return self.attr_summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, CALayerSyntheticProvider)
