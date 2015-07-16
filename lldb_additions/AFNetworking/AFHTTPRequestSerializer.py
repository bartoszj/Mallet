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
from ..Foundation import NSObject
from ..Foundation import NSString
from ..CFNetwork import NSURLRequest
from ..common import SummaryBase


class AFHTTPRequestSerializerSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing AFHTTPRequestSerializer.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFHTTPRequestSerializerSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("string_encoding", ivar_name="_stringEncoding",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_string_encoding_summary)
        self.register_child_value("allows_cellular_access", ivar_name="_allowsCellularAccess",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_allows_cellular_access_summary)
        self.register_child_value("cache_policy", ivar_name="_cachePolicy",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_cache_policy_summary)
        self.register_child_value("http_should_use_pipelining", ivar_name="_HTTPShouldUsePipelining",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_http_should_use_pipelining_summary)
        self.register_child_value("network_service_type", ivar_name="_networkServiceType",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_network_service_type_summary)
        self.register_child_value("timeout_interval", ivar_name="_timeoutInterval",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_timeout_interval_summary)
        self.register_child_value("http_request_headers", ivar_name="_mutableHTTPRequestHeaders",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_http_request_headers_summary)

        self.synthetic_type = self.SYNTHETIC_PROXY_VALUE
        self.synthetic_proxy_value = self.get_proxy_value()

    @staticmethod
    def get_string_encoding_summary(value):
        if value != NSString.NSUTF8StringEncoding:
            summary = NSString.get_string_encoding_text(value)
            return "stringEncoding={}".format(summary)
        return None

    @staticmethod
    def get_allows_cellular_access_summary(value):
        if value:
            return "allowsCellularAccess"
        return None

    @staticmethod
    def get_cache_policy_summary(value):
        if value == NSURLRequest.NSURLRequestUseProtocolCachePolicy:
            return None
        cache_policy = NSURLRequest.get_cache_policy_text(value)
        return "cachePolicy={}".format(cache_policy)

    @staticmethod
    def get_http_should_use_pipelining_summary(value):
        if value:
            return "shouldUsePipelining"
        return None

    @staticmethod
    def get_network_service_type_summary(value):
        if value == NSURLRequest.NSURLNetworkServiceTypeDefault:
            return None
        service_type = NSURLRequest.get_network_service_type_text(value)
        return "networkServiceType={}".format(service_type)

    @staticmethod
    def get_timeout_interval_summary(value):
        if value != 0:
            return "timeout={}".format(SummaryBase.formatted_float(value))
        return None

    @staticmethod
    def get_http_request_headers_summary(value):
        return "HTTPRequestHeaders={}".format(value)

    def get_proxy_value(self):
        """
        Returns proxy value.

        :return: Proxy value.
        :rtype: lldb.SBValue
        """

        http_request_headers = self.http_request_headers
        """:type: lldb.SBValue"""
        http_request_headers_count = self.http_request_headers_value
        if http_request_headers_count == 0:
            return None
        return http_request_headers

    def get_child_index(self, name):
        return None

    def summaries_parts(self):
        return [self.string_encoding_summary,
                self.allows_cellular_access_summary,
                self.cache_policy_summary,
                self.http_should_use_pipelining_summary,
                self.network_service_type_summary,
                self.timeout_interval_summary,
                # self.http_request_headers_summary
                ]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFHTTPRequestSerializerSyntheticProvider)
