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
from ..Foundation import NSObject
import NSURLRequest
import NSURLResponse

NSURLSessionTaskStateRunning = 0
NSURLSessionTaskStateSuspended = 1
NSURLSessionTaskStateCanceling = 2
NSURLSessionTaskStateCompleted = 3

# + Has instance variables.
# - Doesn't have instance variables.
#
# Class hierarchy:
# ┌ NSURLSessionTask (+)
# ├─┬ NSURLSessionDataTask (-)
# │ └── NSURLSessionUploadTask (-)
# ├── NSURLSessionDownloadTask (-)
# ├─┬ __NSCFLocalSessionTask (+)
# │ ├─┬ __NSCFLocalDataTask (-)
# │ │ └── __NSCFLocalUploadTask (-)
# │ └── __NSCFLocalDownloadTask (+)
# └─┬ __NSCFBackgroundSessionTask (+)
#   ├─┬ __NSCFBackgroundDataTask (+)
#   │ └── __NSCFBackgroundUploadTask (-)
#   └── __NSCFBackgroundDownloadTask (+)


class NSURLSessionTaskSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSURLSessionTask.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSURLSessionTaskSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSURLSessionTask"

        self.register_child_value("task_identifier", ivar_name="_taskIdentifier",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
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
        return "tid={}".format(value)

    @staticmethod
    def get_original_request_summary(provider):
        """
        :param NSURLRequest.NSURLRequestSyntheticProvider provider: NSURLRequest provider.
        """
        summary = provider.summary()
        if summary is None or len(summary) == 0:
            return None
        return "request={{{}}}".format(summary)

    @staticmethod
    def get_response_summary(provider):
        """
        :param NSURLResponse.NSURLResponseSyntheticProvider provider: NSURLResponse provider.
        """
        summary = provider.summary()
        if summary is None or len(summary) == 0:
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
        return "{}".format(state)

    def get_received_summary(self):
        """
        Returns short receive summary.

        :return: short receive summary.
        :rtype: str | None
        """
        received = self.count_of_bytes_received_value if self.count_of_bytes_received_value is not None else 0
        to_receive = self.count_of_bytes_expected_to_receive_value if self.count_of_bytes_expected_to_receive_value is not None else 0
        valid_received = False if (received == 0 or received == -1) else True
        valid_to_receive = False if (to_receive == 0 or to_receive == -1) else True

        if valid_received and valid_to_receive:
            return "received={}/{}".format(received, to_receive)
        elif valid_received:
            return "received={}".format(received)
        elif valid_to_receive:
            return "toReceive={}".format(to_receive)
        return None

    def get_sent_summary(self):
        """
        Returns short send summary.

        :return: short send summary.
        :rtype: str | None
        """
        sent = self.count_of_bytes_sent_value if self.count_of_bytes_sent_value is not None else 0
        to_send = self.count_of_bytes_expected_to_send_value if self.count_of_bytes_expected_to_send_value is not None else 0
        valid_sent = False if (sent == 0 or self == -1) else True
        valid_to_send = False if (to_send == 0 or to_send == -1) else True

        if valid_sent and valid_to_send:
            return "sent={}/{}".format(sent, to_send)
        elif valid_sent:
            return "sent={}".format(sent)
        elif valid_to_send:
            return "toSend={}".format(to_send)
        return None

    def summaries_parts(self):
        return [self.state_summary,
                # self.task_identifier_summary,
                self.get_received_summary(),
                self.get_sent_summary(),
                self.original_request_summary,
                self.response_summary,
                # self.task_description_summary
                ]


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
