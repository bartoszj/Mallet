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
from ..Foundation import NSObject
import NSURLResponseInternal


class NSURLResponseSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSURLResponse.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSURLResponseSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSURLResponse"

        self.register_child_value("response_internal", ivar_name="_internal",
                                  provider_class=NSURLResponseInternal.NSURLResponseInternalSyntheticProvider,
                                  summary_function=self.get_response_internal_summary)

        self.synthetic_type = self.SYNTHETIC_PROXY_VALUE
        self.synthetic_proxy_value = self.get_proxy_value()

    @staticmethod
    def get_response_internal_summary(provider):
        """
        :param NSURLResponseInternal.NSURLResponseInternalSyntheticProvider provider: NSURLResponseInternal provider.
        """
        return provider.summary()

    def get_proxy_value(self):
        """
        Returns proxy value.

        :return: Proxy value.
        :rtype: lldb.SBValue
        """
        response_internal = self.response_internal_provider
        """:type: NSURLResponseInternal.NSURLResponseInternalSyntheticProvider"""
        request = response_internal.response_provider
        """:type: CFURLRequest.CFURLRequestSyntheticProvider"""
        http_message_content = request.http_message_content_provider
        """:type: CFHTTPMessage.CFHTTPMessageContentSyntheticProvider"""
        headers_dict = http_message_content.get_http_header_dict_provider()
        headers_count = headers_dict.all_http_header_fields_value

        if headers_count is None or headers_count == 0:
            return None
        return headers_dict.all_http_header_fields

    def get_child_index(self, name):
        return None

    def summary(self):
        return self.response_internal_summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSURLResponseSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category CFNetwork \
                            NSURLResponse".format(__name__))
    debugger.HandleCommand("type synthetic add -l {}.NSURLResponseSyntheticProvider \
                           --category CFNetwork \
                           NSURLResponse NSHTTPURLResponse".format(__name__))
    debugger.HandleCommand("type category enable CFNetwork")
