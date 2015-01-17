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

NSLayoutRelationLessThanOrEqual = 3
NSLayoutRelationEqual = 0
NSLayoutRelationGreaterThanOrEqual = 1

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
NSLayoutAttributeLastBaseline = NSLayoutAttributeBaseline
NSLayoutAttributeFirstBaseline = 12
NSLayoutAttributeLeftMargin = 13
NSLayoutAttributeRightMargin = 14
NSLayoutAttributeTopMargin = 15
NSLayoutAttributeBottomMargin = 16
NSLayoutAttributeLeadingMargin = 17
NSLayoutAttributeTrailingMargin = 18
NSLayoutAttributeCenterXWithinMargins = 19
NSLayoutAttributeCenterYWithinMargins = 20


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
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_coefficient_summary)
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
    def get_coefficient_summary(value):
        if value == 1:
            return ""
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
    def get_second_item_flags(all_flags):
        if all_flags is None:
            return 0
        return (all_flags >> 8) & 0b11111111

    @staticmethod
    def get_attribute_name(flags):
        if flags is None:
            return ""
        elif flags == NSLayoutAttributeNotAnAttribute:
            return ""
        elif flags == NSLayoutAttributeLeft:
            return "left"
        elif flags == NSLayoutAttributeRight:
            return "right"
        elif flags == NSLayoutAttributeTop:
            return "top"
        elif flags == NSLayoutAttributeBottom:
            return "bottom"
        elif flags == NSLayoutAttributeLeading:
            return "leading"
        elif flags == NSLayoutAttributeTrailing:
            return "trailing"
        elif flags == NSLayoutAttributeWidth:
            return "width"
        elif flags == NSLayoutAttributeHeight:
            return "height"
        elif flags == NSLayoutAttributeCenterX:
            return "centerX"
        elif flags == NSLayoutAttributeCenterY:
            return "centerY"
        elif flags == NSLayoutAttributeLastBaseline:
            return "lastBaseline"
        elif flags == NSLayoutAttributeFirstBaseline:
            return "firstBaseline"
        elif flags == NSLayoutAttributeLeftMargin:
            return "leftMargin"
        elif flags == NSLayoutAttributeRightMargin:
            return "rightMargin"
        elif flags == NSLayoutAttributeTopMargin:
            return "topMargin"
        elif flags == NSLayoutAttributeBottomMargin:
            return "bottomMargin"
        elif flags == NSLayoutAttributeLeadingMargin:
            return "leadingMargin"
        elif flags == NSLayoutAttributeTrailingMargin:
            return "trailingMargin"
        elif flags == NSLayoutAttributeCenterXWithinMargins:
            return "centerXWithMargins"
        elif flags == NSLayoutAttributeCenterYWithinMargins:
            return "centerYWithMargins"
        else:
            return "unknown ({})".format(flags)

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

    def print_parameters(self):
        first_item = self.first_item_value
        second_item = self.second_item_value
        multiplier = self.coefficient_value
        multiplier_summary = self.coefficient_summary
        constant = self.constant_value
        constant_summary = self.constant_summary
        priority = self.priority_value
        priority_summary = self.priority_summary
        all_flags = self.layout_constraint_flags_value
        first_item_flags = self.get_first_item_flags(all_flags)
        first_item_attribute = self.get_attribute_name(first_item_flags)
        second_item_flags = self.get_second_item_flags(all_flags)
        second_item_attribute = self.get_attribute_name(second_item_flags)
        relation_flags = self.get_relation_flags(all_flags)
        relation_summary = self.get_relation_summary(relation_flags)
        relation_sign = self.get_relation_sign(relation_flags)

        print("all_flags         : {} {}".format(all_flags, bin(all_flags)))
        print("first_item        : {}".format(first_item))
        print("second_item       : {}".format(second_item))
        print("first_item_flags  : {} {} {}".format(first_item_attribute, first_item_flags, bin(first_item_flags)))
        print("second_item_flags : {} {} {}".format(second_item_attribute, second_item_flags, bin(second_item_flags)))
        print("relation          : {} {}".format(relation_flags, relation_sign))
        print("multiplier        : {} {}".format(multiplier, multiplier_summary))
        print("constant          : {} {}".format(constant, constant_summary))
        print("priority          : {} {}".format(priority, priority_summary))
        print("lowered_constant  : {}".format(self.lowered_constant_value))
        print("==============================")

    def long_summary(self):
        first_item = self.first_item_value
        second_item = self.second_item_value
        multiplier = self.coefficient_value
        multiplier_summary = self.coefficient_summary
        constant = self.constant_value
        constant_summary = self.constant_summary
        priority = self.priority_value
        priority_summary = self.priority_summary
        all_flags = self.layout_constraint_flags_value
        first_item_flags = self.get_first_item_flags(all_flags)
        first_item_attribute = self.get_attribute_name(first_item_flags)
        second_item_flags = self.get_second_item_flags(all_flags)
        second_item_attribute = self.get_attribute_name(second_item_flags)
        relation_flags = self.get_relation_flags(all_flags)
        relation_summary = self.get_relation_summary(relation_flags)
        relation_sign = self.get_relation_sign(relation_flags)

        # Unsupported combination.
        if first_item is None or first_item_flags == NSLayoutAttributeNotAnAttribute:
            return None

        summary = None
        # Constraints not dependent on second item.
        if second_item is None:
            if first_item_flags == NSLayoutAttributeWidth:
                summary = "H:[{}({}{}{})]".format(first_item, relation_summary, constant_summary, priority_summary)
            elif first_item_flags == NSLayoutAttributeHeight:
                summary = "V:[{}({}{}{})]".format(first_item, relation_summary, constant_summary, priority_summary)
        # Constraints dependent on second item.
        else:
            multiplier_part = ""
            if multiplier != 1:
                multiplier_part = "{}*".format(multiplier_summary)

            constant_part = ""
            if constant != 0:
                constant_abs = abs(constant)
                if constant < 0:
                    constant_part = " - {}".format(SummaryBase.formatted_float(constant_abs))
                else:
                    constant_part = " + {}".format(SummaryBase.formatted_float(constant_abs))

            priority_part = ""
            if priority != 1000:
                priority_part = " {}".format(priority_summary)

            summary = "{}.{} {} {}{}.{}{}{}".format(first_item, first_item_attribute,
                                                    relation_sign, multiplier_part,
                                                    second_item, second_item_attribute,
                                                    constant_part, priority_part)

        return summary

    def short_summary(self):
        first_item = self.first_item_value
        second_item = self.second_item_value
        multiplier = self.coefficient_value
        multiplier_summary = self.coefficient_summary
        constant = self.constant_value
        constant_summary = self.constant_summary
        priority = self.priority_value
        priority_summary = self.priority_summary
        all_flags = self.layout_constraint_flags_value
        first_item_flags = self.get_first_item_flags(all_flags)
        first_item_attribute = self.get_attribute_name(first_item_flags)
        second_item_flags = self.get_second_item_flags(all_flags)
        second_item_attribute = self.get_attribute_name(second_item_flags)
        relation_flags = self.get_relation_flags(all_flags)
        relation_summary = self.get_relation_summary(relation_flags)
        relation_sign = self.get_relation_sign(relation_flags)

        # Unsupported combination.
        if first_item is None or first_item_flags == NSLayoutAttributeNotAnAttribute:
            return None

        summary = None
        # Constraints not dependent on second item.
        if second_item is None:
            if first_item_flags == NSLayoutAttributeWidth:
                summary = "H:[{}({}{}{})]".format(first_item, relation_summary, constant_summary, priority_summary)
            elif first_item_flags == NSLayoutAttributeHeight:
                summary = "V:[{}({}{}{})]".format(first_item, relation_summary, constant_summary, priority_summary)
        # Constraints dependent on second item.
        else:
            multiplier_part = ""
            if multiplier != 1:
                multiplier_part = "{}*".format(multiplier_summary)

            constant_part = ""
            if constant != 0:
                constant_abs = abs(constant)
                if constant < 0:
                    constant_part = " - {}".format(SummaryBase.formatted_float(constant_abs))
                else:
                    constant_part = " + {}".format(SummaryBase.formatted_float(constant_abs))

            priority_part = ""
            if priority != 1000:
                priority_part = " {}".format(priority_summary)

            summary = "{} {} {}{}{}{}".format(first_item_attribute,
                                              relation_sign, multiplier_part,
                                              second_item_attribute,
                                              constant_part, priority_part)

        return summary

    def summary(self):
        # self.print_parameters()
        # return self.short_summary()
        return self.long_summary()


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSLayoutConstraintSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category Foundation \
                            NSLayoutConstraint".format(__name__))
    debugger.HandleCommand("type category enable UIKit")
