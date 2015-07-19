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

from .. import helpers
from ..common import SummaryBase
import NSObject
import NSOperation
import NSOperationInternal


class NSOperationQueueInternalSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing __NSOperationQueueInternal.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSOperationQueueInternalSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "__NSOperationQueueInternal"

        self.register_child_value("first_operation", ivar_name="__firstOperation",
                                  provider_class=NSOperation.NSOperationSyntheticProvider,
                                  summary_function=self.get_first_operation_summary)
        self.register_child_value("last_operation", ivar_name="__lastOperation",
                                  provider_class=NSOperation.NSOperationSyntheticProvider,
                                  summary_function=self.get_last_operation_summary)
        self.register_child_value("pending_first_operation", ivar_name="__pendingFirstOperation",
                                  provider_class=NSOperation.NSOperationSyntheticProvider,
                                  summary_function=self.get_pending_first_operation_summary)
        self.register_child_value("pending_last_operation", ivar_name="__pendingLastOperation",
                                  provider_class=NSOperation.NSOperationSyntheticProvider,
                                  summary_function=self.get_pending_last_operation_summary)
        self.register_child_value("max_operations_count", ivar_name="__maxNumOps",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_max_operation_count_summary)
        self.register_child_value("actual_max_operations_count", ivar_name="__actualMaxNumOps",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_actual_max_operations_count_summary)
        self.register_child_value("executing_operations_count", ivar_name="__numExecOps",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_executing_operations_count_summary)
        self.register_child_value("main", ivar_name="__mainQ",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_main_summary)
        self.register_child_value("suspended", ivar_name="__suspended",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_suspended_summary)
        self.register_child_value("over_commit", ivar_name="__overcommit",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_over_commit_summary)
        self.register_child_value("qos", ivar_name="__propertyQOS",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_qos_summary)
        self.register_child_value("name", ivar_name="__nameBuffer",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_name_summary)

    @staticmethod
    def get_first_operation_summary(provider):
        """
        :param NSOperation.NSOperationSyntheticProvider provider: NSOperation provider.
        :return: NSOperation summary/
        :rtype: str | None
        """
        return "first={}".format(provider.summary())

    @staticmethod
    def get_last_operation_summary(provider):
        """
        :param NSOperation.NSOperationSyntheticProvider provider: NSOperation provider.
        :return: NSOperation summary/
        :rtype: str | None
        """
        return "last={}".format(provider.summary())

    @staticmethod
    def get_pending_first_operation_summary(provider):
        """
        :param NSOperation.NSOperationSyntheticProvider provider: NSOperation provider.
        :return: NSOperation summary/
        :rtype: str | None
        """
        return "pending_first={}".format(provider.summary())

    @staticmethod
    def get_pending_last_operation_summary(provider):
        """
        :param NSOperation.NSOperationSyntheticProvider provider: NSOperation provider.
        :return: NSOperation summary/
        :rtype: str | None
        """
        return "pending_last={}".format(provider.summary())

    @staticmethod
    def get_max_operation_count_summary(value):
        if value == -1:
            return None
        return "max={}".format(value)

    @staticmethod
    def get_actual_max_operations_count_summary(value):
        return "actual={}".format(value)

    @staticmethod
    def get_executing_operations_count_summary(value):
        return "executing={}".format(value)

    @staticmethod
    def get_main_summary(value):
        if value:
            return "mainQueue"
        return None

    @staticmethod
    def get_suspended_summary(value):
        if value:
            return "suspended"
        return None

    @staticmethod
    def get_over_commit_summary(value):
        return "over_commit={}".format(value)

    @staticmethod
    def get_qos_summary(value):
        qos = NSOperationInternal.get_qos_text(value)
        if qos is None:
            return None
        return "qos={}".format(qos)

    @staticmethod
    def get_name_summary(value):
        return "name={}".format(value)

    def get_operations_count(self):
        """
        Returns operations count.
        :return: Operations count.
        :rtype: int
        """
        addresses = set()

        # Get first operation.
        operation = self.first_operation
        """:type: lldb.SBValue"""
        operation_value = SummaryBase.get_unsigned_value(operation)
        if operation_value == 0:
            operation = self.pending_first_operation
            """:type: lldb.SBValue"""
            operation_value = SummaryBase.get_unsigned_value(operation)

        # Add operation address to set.
        while operation_value != 0:
            addresses.add(operation_value)

            # Get next operation.
            operation_provider = NSOperation.NSOperationSyntheticProvider(operation, self.internal_dict)
            operation_internal_provider = operation_provider.private_provider
            """:type: NSOperationInternal.NSOperationInternalSyntheticProvider"""
            operation = operation_internal_provider.next_operation
            operation_value = SummaryBase.get_unsigned_value(operation)

        return len(addresses)

    def get_operations_count_summary(self):
        count = self.get_operations_count()
        return "operations={}".format(count)

    def summaries_parts(self):
        return [self.suspended_summary,
                self.get_operations_count_summary(),
                self.executing_operations_count_summary,
                self.max_operations_count_summary,
                self.qos_summary,
                self.main_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSOperationQueueInternalSyntheticProvider)
