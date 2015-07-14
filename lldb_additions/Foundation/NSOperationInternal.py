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
import NSOperationQueue

NSQualityOfServiceUserInteractive = 0x21
NSQualityOfServiceUserInitiated = 0x19
NSQualityOfServiceUtility = 0x11
NSQualityOfServiceBackground = 0x09
NSQualityOfServiceDefault = -1

NSOperationQueuePriorityVeryLow = -8
NSOperationQueuePriorityLow = -4
NSOperationQueuePriorityNormal = 0
NSOperationQueuePriorityHigh = 4
NSOperationQueuePriorityVeryHigh = 8


class NSOperationInternalSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSOperationInternal.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSOperationInternalSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.module_name = "Foundation"
        self.type_name = "__NSOperationInternal"

        self.register_child_value("outer_operation", ivar_name="__outerOp",
                                  provider_class=NSOperation.NSOperationSyntheticProvider)
        self.register_child_value("previous_operation", ivar_name="__prevOp",
                                  provider_class=NSOperation.NSOperationSyntheticProvider)
        self.register_child_value("next_operation", ivar_name="__nextOp",
                                  provider_class=NSOperation.NSOperationSyntheticProvider)
        self.register_child_value("next_priority_operation", ivar_name="__nextPriOp",
                                  provider_class=NSOperation.NSOperationSyntheticProvider)
        self.register_child_value("queue", ivar_name="__queue",
                                  provider_class=NSOperationQueue.NSOperationQueueSyntheticProvider)
        self.register_child_value("sequential_number", ivar_name="__seqno",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_sequential_number_summary)
        self.register_child_value("thread_priority", ivar_name="__thread_prio",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_thread_priority_summary)
        self.register_child_value("rc", ivar_name="__RC",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_rc_summary)
        self.register_child_value("state", ivar_name="__state",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_state_summary)
        self.register_child_value("priority", ivar_name="__prio",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_priority_summary)
        self.register_child_value("ready", ivar_name="__cached_isReady",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_ready_summary)
        self.register_child_value("cancelled", ivar_name="__isCancelled",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_cancelled_summary)
        self.register_child_value("barrier", ivar_name="__isBarrier",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_barrier_summary)
        self.register_child_value("qos", ivar_name="__qoses",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_qos_summary)
        self.register_child_value("name", ivar_name="__nameBuffer",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_name_summary)

    @staticmethod
    def get_sequential_number_summary(value):
        return "sequentialNumber={}".format(value)

    @staticmethod
    def get_thread_priority_summary(value):
        return "threadPriority={}".format(value)

    @staticmethod
    def get_rc_summary(value):
        return "rc={}".format(value)

    @staticmethod
    def get_state_summary(value):
        return "state={}".format(value)

    @staticmethod
    def get_priority_summary(value):
        if value == -1:
            return None
        priority = get_priority_text(value)
        return "priority={}".format(priority)

    @staticmethod
    def get_ready_summary(value):
        if value:
            return "ready"
        return None

    @staticmethod
    def get_cancelled_summary(value):
        if value:
            return "cancelled"
        return None

    @staticmethod
    def get_barrier_summary(value):
        return "barrier={}".format(value)

    @staticmethod
    def get_qos_summary(value):
        value &= 0xFF
        qos = get_qos_text(value)
        if qos is None:
            return None
        return "qos={}".format(qos)

    @staticmethod
    def get_name_summary(value):
        return "name={}".format(value)

    def summaries_parts(self):
        return [self.cancelled_summary,
                self.priority_summary,
                self.qos_summary,
                self.name_summary]


def get_qos_text(qos):
    """
    Returns QOS name by numeric value.

    :param int qos: QOS numeric value.
    :return: QOS name.
    :rtype: str | None
    """
    if qos == NSQualityOfServiceUserInteractive:
        return "UserInteractive"
    elif qos == NSQualityOfServiceUserInitiated:
        return "UserInitiated"
    elif qos == NSQualityOfServiceUtility:
        return "Utility"
    elif qos == NSQualityOfServiceBackground:
        return "Background"
    elif qos == NSQualityOfServiceDefault:
        return "Default"
    return None


def get_priority_text(priority):
    """
    Returns operation priority name by numeric value.

    :param int priority: Priority numeric value.
    :return: Operation priority name.
    :rtype: str | None
    """
    if priority == NSOperationQueuePriorityVeryLow:
        return "VeryLow"
    elif priority == NSOperationQueuePriorityLow:
        return "Low"
    elif priority == NSOperationQueuePriorityNormal:
        return "Normal"
    elif priority == NSOperationQueuePriorityHigh:
        return "High"
    elif priority == NSOperationQueuePriorityVeryHigh:
        return "VeryHigh"
    return "{}".format(priority)


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSOperationInternalSyntheticProvider)
