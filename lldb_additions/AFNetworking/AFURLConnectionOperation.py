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
from ..Foundation import NSOperation
from ..CFNetwork import NSURLRequest
from ..CFNetwork import NSURLResponse
from ..CFNetwork import NSURLConnection
from .. import SummaryBase

AFOperationPausedState = -1
AFOperationReadyState = 1
AFOperationExecutingState = 2
AFOperationFinishedState = 3


class AFURLConnectionOperationSyntheticProvider(NSOperation.NSOperationSyntheticProvider):
    """
    Class representing AFURLConnectionOperation.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFURLConnectionOperationSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("state", ivar_name="_state",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_state_summary)
        self.register_child_value("connection", ivar_name="_connection",
                                  provider_class=NSURLConnection.NSURLConnectionSyntheticProvider,
                                  summary_function=self.get_connection_summary)
        self.register_child_value("request", ivar_name="_request",
                                  provider_class=NSURLRequest.NSURLRequestSyntheticProvider,
                                  summary_function=self.get_request_summary)
        self.register_child_value("response", ivar_name="_response",
                                  provider_class=NSURLResponse.NSURLResponseSyntheticProvider,
                                  summary_function=self.get_response_summary)
        self.register_child_value("response_data", ivar_name="_responseData",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_response_data_summary)
        self.register_child_value("response_string", ivar_name="_responseString",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_response_string_summary)
        self.register_child_value("total_bytes_read", ivar_name="_totalBytesRead",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_total_bytes_read_summary)
        self.register_child_value("background_task_identifier", ivar_name="_backgroundTaskIdentifier",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_background_task_identifier_summary)
        self.register_child_value("should_use_credential_storage", ivar_name="_shouldUseCredentialStorage",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_should_use_credential_storage_summary)

    @staticmethod
    def get_state_summary(value):
        state_text = get_state_text(value)
        return "{}".format(state_text)

    @staticmethod
    def get_connection_summary(provider):
        """
        :param NSURLConnection.NSURLConnectionSyntheticProvider provider: NSURLConnection provider.
        :return: str | None
        """
        summary = provider.summary()
        if summary is None or len(summary) == 0:
            return None
        return "connection={{{}}}".format(summary)

    @staticmethod
    def get_request_summary(provider):
        """
        :param NSURLRequest.NSURLRequestSyntheticProvider provider: NSURLRequest provider
        :return: str | None
        """
        summary = provider.summary()
        if summary is None or len(summary) == 0:
            return None
        return "request={{{}}}".format(summary)

    @staticmethod
    def get_response_summary(provider):
        """
        :param NSURLResponse.NSURLResponseSyntheticProvider provider: NSURLResponse provider.
        :return: str | None
        """
        summary = provider.summary()

        if summary is None or len(summary) == 0:
            return None
        return "response={{{}}}".format(summary)

    @staticmethod
    def get_response_data_summary(value):
        return "responseData={}".format(value)

    @staticmethod
    def get_response_string_summary(value):
        return "responseString={}".format(value)

    @staticmethod
    def get_total_bytes_read_summary(value):
        if value == 0:
            return None
        return "totalBytesRead={}".format(value)

    @staticmethod
    def get_background_task_identifier_summary(value):
        if value == 0:
            return None
        return "BID={}".format(value)

    @staticmethod
    def get_should_use_credential_storage_summary(value):
        return "shouldUseCredentialStorage={}".format(value)

    def summaries_parts(self):
        return [self.state_summary,
                self.response_data_summary,
                self.request_summary,
                self.response_summary]


def get_state_text(state):
    """
    Returns AFURLConnectionOperation state text.

    :param int state: State numeric value.
    :return: AFURLConnectionOperation state text.
    :rtype: str
    """
    if state == AFOperationPausedState:
        return "Paused"
    elif state == AFOperationReadyState:
        return "Ready"
    elif state == AFOperationExecutingState:
        return "Executing"
    elif state == AFOperationFinishedState:
        return "Finished"
    else:
        return "Unknown"


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFURLConnectionOperationSyntheticProvider)
