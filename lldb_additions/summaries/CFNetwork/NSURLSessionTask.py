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
import NSURLRequest
import NSURLResponse

NSURLSessionTaskStateRunning = 0
NSURLSessionTaskStateSuspended = 1
NSURLSessionTaskStateCanceling = 2
NSURLSessionTaskStateCompleted = 3

# Class hierarchy:
# ┌ NSURLSessionTask (+)
# ├── NSURLSessionDataTask (-)
# ├── NSURLSessionDownloadTask (-)
# ├── NSURLSessionUploadTask (-)
# └─┬ __NSCFLocalSessionTask (+)
#   ├── __NSCFLocalDataTask (-)
#   ├── __NSCFLocalDownloadTask (+)
#   └── __NSCFLocalUploadTask (-)


class NSURLSessionTaskSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSURLSessionTask.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSURLSessionTaskSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSURLSessionTask"

        self.register_child_value("task_identifier", ivar_name="_taskIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_task_identifier_summary)
        self.register_child_value("original_request", ivar_name="_originalRequest",
                                  provider_class=NSURLRequest.NSURLRequestSyntheticProvider,
                                  summary_function=self.get_original_request_summary)
        self.register_child_value("response", ivar_name="_response",
                                  provider_class=NSURLResponse.NSURLResponseSyntheticProvider,
                                  summary_function=self.get_response_summary)
        self.register_child_value("count_of_bytes_received", ivar_name="_countOfBytesReceived",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_count_of_bytes_received_summary)
        self.register_child_value("count_of_bytes_sent", ivar_name="_countOfBytesSent",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_count_of_bytes_sent_summary)
        self.register_child_value("count_of_bytes_expected_to_send", ivar_name="_countOfBytesExpectedToSend",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_count_of_bytes_expected_to_send_summary)
        self.register_child_value("count_of_bytes_expected_to_receive", ivar_name="_countOfBytesExpectedToReceive",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_count_of_bytes_expected_to_receive_summary)
        self.register_child_value("task_description", ivar_name="_taskDescription",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_task_description_summary)
        self.register_child_value("state", ivar_name="_state",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_state_summary)

    @staticmethod
    def get_task_identifier_summary(value):
        return "taskIdentifier={}".format(value)

    @staticmethod
    def get_original_request_summary(provider):
        """
        :param NSURLRequest.NSURLRequestSyntheticProvider provider: NSURLRequest provider.
        """
        summary = provider.summary()
        if len(summary) == 0:
            return None
        return "request={{{}}}".format(summary)

    @staticmethod
    def get_response_summary(provider):
        """
        :param NSURLResponse.NSURLResponseSyntheticProvider provider: NSURLResponse provider.
        """
        summary = provider.summary()
        if len(summary) == 0:
            return None
        return "response={{{}}}".format(summary)

    @staticmethod
    def get_count_of_bytes_received_summary(value):
        if value == 0 or value == -1:
            return None
        return "received={}".format(value)

    @staticmethod
    def get_count_of_bytes_sent_summary(value):
        if value == 0 or value == -1:
            return None
        return "sent={}".format(value)

    @staticmethod
    def get_count_of_bytes_expected_to_send_summary(value):
        if value == 0 or value == -1:
            return None
        return "toSend={}".format(value)

    @staticmethod
    def get_count_of_bytes_expected_to_receive_summary(value):
        if value == 0 or value == -1:
            return None
        return "toReceive={}".format(value)

    @staticmethod
    def get_task_description_summary(value):
        return "taskDescription={}".format(value)

    @staticmethod
    def get_state_summary(value):
        state = get_session_task_state_text(value)
        return "state={}".format(state)

    def summary(self):
        summary = SummaryBase.join_summaries(self.state_summary,
                                             self.count_of_bytes_received_summary,
                                             self.count_of_bytes_expected_to_receive_summary,
                                             self.count_of_bytes_sent_summary,
                                             self.count_of_bytes_expected_to_send_summary,
                                             self.task_identifier_summary,
                                             self.original_request_summary,
                                             self.response_summary,
                                             self.task_description_summary)
        return summary


def get_session_task_state_text(value):
    if value == NSURLSessionTaskStateRunning:
        return "Running"
    elif value == NSURLSessionTaskStateSuspended:
        return "Suspended"
    elif value == NSURLSessionTaskStateCanceling:
        return "Canceling"
    elif value == NSURLSessionTaskStateCompleted:
        return "Completed"
    return "Unknown"


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSURLSessionTaskSyntheticProvider)
