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
from ..Foundation import NSOperationQueue
import NSURLConnection
import NSURLRequest


class NSURLConnectionInternalSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSURLConnectionInternal.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSURLConnectionInternalSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.module_name = "CFNetwork"
        self.type_name = "NSURLConnectionInternal"

        self.register_child_value("connection", ivar_name="_connection",
                                  provider_class=NSURLConnection.NSURLConnectionSyntheticProvider)
        self.register_child_value("delegate_queue", ivar_name="_delegateQueue",
                                  provider_class=NSOperationQueue.NSOperationQueueSyntheticProvider)
        self.register_child_value("url", ivar_name="_url",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_url_summary)
        self.register_child_value("original_request", ivar_name="_originalRequest",
                                  provider_class=NSURLRequest.NSURLRequestSyntheticProvider,
                                  summary_function=self.get_original_request_summary)
        self.register_child_value("current_request", ivar_name="_currentRequest",
                                  provider_class=NSURLRequest.NSURLRequestSyntheticProvider,
                                  summary_function=self.get_current_request_summary)
        self.register_child_value("connection_active", ivar_name="_connectionActive",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_connection_active_summary)

    @staticmethod
    def get_url_summary(value):
        return "url={}".format(value)

    @staticmethod
    def get_original_request_summary(provider):
        """
        :param NSURLRequest.NSURLRequestSyntheticProvider provider: NSURLRequest provider.
        """
        return "original={}".format(provider.summary())

    @staticmethod
    def get_current_request_summary(provider):
        """
        :param NSURLRequest.NSURLRequestSyntheticProvider provider: NSURLRequest provider.
        """
        return "current={}".format(provider.summary())

    @staticmethod
    def get_connection_active_summary(value):
        if value:
            return "active"
        return None

    def summaries_parts(self):
        return [self.url_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSURLConnectionInternalSyntheticProvider)
