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
from .. import SummaryBase
from ..Foundation import NSObject
import lldb


class UIColorSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UIColor.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIColorSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIColor"

        self.register_child_value("system_color_name", ivar_name="_systemColorName",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_system_color_name_summary)

        self.synthetic_children = ["system_color_name"]

    @staticmethod
    def get_system_color_name_summary(value):
        return "systemColorName={}".format(value)

    def summary(self):
        return self.system_color_name_summary


class UIColorSubclassesSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Proxy class calling correct synthetic child class.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIColorSubclassesSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.color_class_name = helpers.get_object_class_name(value_obj)
        if self.color_class_name == "UIDeviceWhiteColor" or self.color_class_name == "UICachedDeviceWhiteColor":
            import UIDeviceWhiteColor
            self.color_proxy = UIDeviceWhiteColor.UIDeviceWhiteColorSyntheticProvider(value_obj, internal_dict)
        elif self.color_class_name == "UIDeviceRGBColor" or self.color_class_name == "UICachedDeviceRGBColor":
            import UIDeviceRGBColor
            self.color_proxy = UIDeviceRGBColor.UIDeviceRGBColorSyntheticProvider(value_obj, internal_dict)
        else:
            self.color_proxy = UIColorSyntheticProvider(value_obj, internal_dict)

    def num_children(self):
        return self.color_proxy.num_children()

    def get_child_index(self, name):
        return self.color_proxy.get_child_index(name)

    def get_child_at_index(self, index):
        return self.color_proxy.get_child_at_index(index)

    def update(self):
        return self.color_proxy.update()

    def has_children(self):
        return self.color_proxy.has_children()


def summary_provider(value_obj, internal_dict):
    """
    Returns summary for UIColor classes.

    :param lldb.SBValue value_obj: LLDB object value.
    :param dict internal_dict: Internal LLDB dictionary.
    :return: UIColor summary.
    :rtype: str
    """

    class_name = helpers.get_object_class_name(value_obj)

    if class_name == "UIDeviceWhiteColor" or class_name == "UICachedDeviceWhiteColor":
        import UIDeviceWhiteColor
        return helpers.generic_summary_provider(value_obj, internal_dict, UIDeviceWhiteColor.UIDeviceWhiteColorSyntheticProvider)
    elif class_name == "UIDeviceRGBColor" or class_name == "UICachedDeviceRGBColor":
        import UIDeviceRGBColor
        return helpers.generic_summary_provider(value_obj, internal_dict, UIDeviceRGBColor.UIDeviceRGBColorSyntheticProvider)
    else:
        return helpers.generic_summary_provider(value_obj, internal_dict, UIColorSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category UIKit \
                            UIColor".format(__name__))
    debugger.HandleCommand("type synthetic add -l {}.UIColorSubclassesSyntheticProvider \
                           --category UIKit \
                           UIColor".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
