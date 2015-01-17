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

NSLayoutAttributeNotAnAttribute = 0
NSLayoutAttributeLeft = 1
NSLayoutAttributeRight = 2
NSLayoutAttributeTop = 3
NSLayoutAttributeBottom = 4
NSLayoutAttributeLeading = 5
NSLayoutAttributeTrailing = 6
NSLayoutAttributeWidth = 7
NSLayoutAttributeHeight = 8
NSLayoutAttributeCenterX = 9
NSLayoutAttributeCenterY = 10
NSLayoutAttributeBaseline = 11

NSLayoutRelationLessThanOrEqual = 3
NSLayoutRelationEqual = 0
NSLayoutRelationGreaterThanOrEqual = 1


class NSLayoutConstraintSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSLayoutConstraint.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSLayoutConstraintSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSLayoutConstraint"

        self.register_child_value("container", ivar_name="_container")
        self.register_child_value("first_item", ivar_name="_firstItem",
                                  primitive_value_function=self.get_class_and_address_value)
        self.register_child_value("second_item", ivar_name="_secondItem",
                                  primitive_value_function=self.get_class_and_address_value)
        self.register_child_value("constant", ivar_name="_constant",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_constant_summary)
        self.register_child_value("lowered_constant", ivar_name="_loweredConstant",
                                  primitive_value_function=SummaryBase.get_float_value)
        self.register_child_value("layout_constraint_flags", ivar_name="_layoutConstraintFlags",
                                  primitive_value_function=SummaryBase.get_unsigned_value)
        self.register_child_value("coefficient", ivar_name="_coefficient",
                                  primitive_value_function=SummaryBase.get_float_value)
        self.register_child_value("priority", ivar_name="_priority",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_priority_summary)

    @staticmethod
    def get_class_and_address_value(obj):
        """
        Returns object type (class) and pointer as string from LLDB value.

        :param lldb.SBValue obj: LLDB value object.
        :return: Type and pointer
        :rtype: str | None
        """
        class_name = SummaryBase.get_class_name_value(obj)
        address = SummaryBase.get_unsigned_value(obj)
        if class_name is None or address is None or address == 0:
            return None
        return "{}:{:#x}".format(class_name, address)

    @staticmethod
    def get_constant_summary(value):
        return "{}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_priority_summary(value):
        if value == 1000:
            return ""
        return "@{}".format(SummaryBase.formatted_float(value))

    @staticmethod
    def get_first_item_flags(all_flags):
        if all_flags is None:
            return 0
        return all_flags & 0b11111111

    @staticmethod
    def get_relation_flags(all_flags):
        if all_flags is None:
            return 0
        return all_flags >> 16

    @staticmethod
    def get_relation_sign(value):
        if value is None:
            return ""
        elif value == NSLayoutRelationLessThanOrEqual:
            return "<="
        elif value == NSLayoutRelationEqual:
            return "=="
        else:
            return ">="

    @staticmethod
    def get_relation_summary(value):
        if value is None:
            return ""
        elif value == NSLayoutRelationLessThanOrEqual:
            return "<="
        elif value == NSLayoutRelationEqual:
            return ""
        else:
            return ">="

    def summary(self):
        first_item = self.first_item_value
        second_item = self.second_item_value
        constant = self.constant_summary
        priority = self.priority_summary
        all_flags = self.layout_constraint_flags_value
        first_item_flags = self.get_first_item_flags(all_flags)
        relation_flags = self.get_relation_flags(all_flags)
        relation = self.get_relation_summary(relation_flags)

        # print("first_item:{}".format(first_item))
        # print("second_item:{}".format(second_item))
        # print("constant:{}".format(constant))
        # print("priority:{}".format(priority))
        # print("all_flags:{} {}".format(all_flags, bin(all_flags)))
        # print("first_item_flags:{} {}".format(first_item_flags, bin(first_item_flags)))
        # print("relation:{} {}".format(relation_flags, self.get_relation_sign(relation_flags)))
        # print("lowered_constant:{}".format(self.lowered_constant_value))
        # print("coefficient:{}".format(self.coefficient_value))
        # print("==============================")

        summary = None
        if first_item_flags == NSLayoutAttributeWidth:
            summary = "H:[{}({}{}{})]".format(first_item, relation, constant, priority)
        elif first_item_flags == NSLayoutAttributeHeight:
            summary = "V:[{}({}{}{})]".format(first_item, relation, constant, priority)

        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSLayoutConstraintSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category Foundation \
                            NSLayoutConstraint".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
