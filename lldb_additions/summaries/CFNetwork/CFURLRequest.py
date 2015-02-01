#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Bartosz Janda
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


class CFURLRequestSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing CFURLRequest structure.

    :param int url_offset: Offset to HTTP url.
    :param int http_message_offset: Offset to CFHTTPMessageRef.
    :param int tmp1_offset: Offset to "structure _tmp1"
    :param int http_header_dict_offset1: Offset to HTTPHeaderDict.
    :param int http_header_dict_offset2: Offset to HTTPHeaderDict.
    :param int http_method_offset: Offset to HTTP method.
    :param int http_body_offset: Offset to HTTP body data.
    :param int http_headers_offset: Offset to HTTP headers.
    """
    # CFURLRequest:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSURL *url                                                             20 = 0x14 / 4           40 = 0x28 / 8
    # CFHTTPMessageRef http_message                                          48 = 0x30 / 4           88 = 0x58 / 8

    # CFHTTPMessageRef {
    #     struct _tmp1 *tmp1                                                 24 = 0x18 / 4           48 = 0x30 / 8
    #     HTTPHeaderDict *http_header_dict                                   48 = 0x30 / 4           96 = 0x60 / 8
    #     HTTPHeaderDict *http_header_dict                                   52 = 0x34 / 4          104 = 0x68 / 8
    #     NSString *HTTPMethod                                               68 = 0x44 / 4          136 = 0x88 / 8
    # }

    # struct _tmp1 {
    #     NSData *HTTPBody                                                    8 = 0x08 / 4           16 = 0x10 / 8
    # }

    # HTTPHeaderDict {
    #     NSDictionary *allHTTPHeaderFields                                   4 = 0x08 / 4            8 = 0x08 / 8
    # }

    def __init__(self, value_obj, internal_dict):
        """
        :param lldb.SBValue value_obj: LLDB variable to compute summary.
        :param dict internal_dict: Internal LLDB dictionary.
        """
        super(CFURLRequestSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            self.url_offset = 0x28
            self.http_message_offset = 0x58
            self.tmp1_offset = 0x30
            self.http_header_dict_offset1 = 0x68
            self.http_header_dict_offset2 = 0x60
            self.http_method_offset = 0x88
            self.http_body_offset = 0x10
            self.http_headers_offset = 0x08
        else:
            self.url_offset = 0x14
            self.http_message_offset = 0x30
            self.tmp1_offset = 0x18
            self.http_header_dict_offset1 = 0x34
            self.http_header_dict_offset2 = 0x30
            self.http_method_offset = 0x44
            self.http_body_offset = 0x8
            self.http_headers_offset = 0x04

        self.register_child_value("url", type_name="NSURL *", offset=self.url_offset,
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_url_summary)
        self.register_child_value("http_message", type_name="addr_ptr_type", offset=self.http_message_offset)

        self.http_method = None
        self.tmp1 = None
        self.http_header_dict = None
        self.http_body = None
        self.http_headers = None

    @staticmethod
    def get_url_summary(value):
        """
        Returns URL summary.

        :param str value: URL value.
        :return: URL summary.
        :rtype: str
        """
        return "{}".format(value)

    @helpers.save_parameter("tmp1")
    def get_tmp1(self):
        """
        Returns LLDB value of tmp1 structure.

        :return: LLDB value of tmp1 structure.
        :rtype: lldb.SBValue
        """
        if self.http_message is None:
            return None

        tmp1 = self.http_message.CreateChildAtOffset("tmp1", self.tmp1_offset, self.get_type("addr_ptr_type"))
        return tmp1

    @helpers.save_parameter("http_header_dict")
    def get_http_header_dict(self):
        """
        Returns LLDB value of HTTPHeaderDict.

        :return: LLDB value of HTTPHeaderDict.
        :rtype: lldb.SBValue
        """
        if self.http_message is None:
            return None

        http_header_dict = self.http_message.CreateChildAtOffset("http_header_dict", self.http_header_dict_offset1, self.get_type("addr_ptr_type"))
        """:type: lldb.SBValue"""
        value = SummaryBase.get_signed_value(http_header_dict)
        if value is None or value == 0:
            http_header_dict = self.http_message.CreateChildAtOffset("http_header_dict", self.http_header_dict_offset2, self.get_type("addr_ptr_type"))
            """:type: lldb.SBValue"""

        return http_header_dict

    @helpers.save_parameter("http_method")
    def get_http_method(self):
        """
        Returns LLDB object representing HTTP method.

        :return: LLDB object representing HTTP method.
        :rtype: lldb.SBValue
        """
        if self.http_message is None:
            return None
        return self.http_message.CreateChildAtOffset("HTTPMethod", self.http_method_offset, self.get_type("NSString *"))

    def get_http_method_value(self):
        """
        Returns HTTP method value.

        :return: HTTP method value.
        :rtype: str
        """
        return SummaryBase.get_stripped_summary_value(self.get_http_method())

    def get_http_method_summary(self):
        """
        Returns HTTP method summary.

        :return: HTTP method summary.
        :rtype: str
        """
        method_value = self.get_http_method_value()
        return None if method_value is None else "{}".format(method_value)

    @helpers.save_parameter("http_body")
    def get_http_body(self):
        """
        Returns LLDB object representing HTTP body data.

        :return: LLDB object representing HTTP body data.
        :rtype: lldb.SBValue
        """
        tmp1 = self.get_tmp1()
        if tmp1 is None:
            return None

        return tmp1.CreateChildAtOffset("HTTPBody", self.http_body_offset, self.get_type("NSData *"))

    def get_http_body_value(self):
        """
        Returns HTTP body value.

        :return: HTTP body value.
        :rtype: str
        """
        return SummaryBase.get_summary_value(self.get_http_body())

    def get_http_body_summary(self):
        """
        Returns HTTP body summary.

        :return: HTTP body summary.
        :rtype: str
        """
        value = self.get_http_body_value()
        return None if value is None else "body={}".format(value)

    @helpers.save_parameter("http_headers")
    def get_http_headers(self):
        """
        Returns LLDB object representing HTTP headers.

        :return: LLDB object representing HTTP headers.
        :rtype: lldb.SBValue
        """
        http_header_dict = self.get_http_header_dict()
        if http_header_dict is None:
            return None

        return http_header_dict.CreateChildAtOffset("allHTTPHeaderFields", self.http_headers_offset, self.get_type("NSDictionary *"))

    def get_http_headers_value(self):
        """
        Returns HTTP headers value.

        :return: HTTP headers value.
        :rtype: str
        """
        return SummaryBase.get_synthetic_count_value(self.get_http_headers())

    def get_http_headers_summary(self):
        """
        Returns HTTP headers summary.

        :return: HTTP headers summary.
        :rtype: str
        """
        value = self.get_http_headers_value()
        if value is None or value == 0:
            return None
        return "headers={}".format(value)

    def summary(self):
        summary = SummaryBase.join_summaries(self.get_http_method_summary(), self.url_summary, self.get_http_body_summary())
        return summary


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, CFURLRequestSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category CFNetwork \
                            _CFURLRequest".format(__name__))
    debugger.HandleCommand("type category enable CFNetwork")
