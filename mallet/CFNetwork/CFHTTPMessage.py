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

from ..common import SummaryBase
import HTTPHeaderDict


class CFHTTPMessageContentSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing CFHTTPMessage structure content.

    :param int tmp1_offset: Offset to "structure _tmp1"
    :param int http_header_dict_offset1: Offset to HTTPHeaderDict.
    :param int http_header_dict_offset2: Offset to HTTPHeaderDict.
    :param int http_method_offset: Offset to HTTP method.
    """
    # CFHTTPMessageContent:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # struct _tmp1 *tmp1                                                     24 = 0x18 / 4           48 = 0x30 / 8
    # HTTPHeaderDict *http_header_dict1                                      48 = 0x30 / 4           96 = 0x60 / 8
    # HTTPHeaderDict *http_header_dict2                                      52 = 0x34 / 4          104 = 0x68 / 8
    # NSString *HTTPMethod                                                   68 = 0x44 / 4          136 = 0x88 / 8

    def __init__(self, value_obj, internal_dict):
        """
        :param lldb.SBValue value_obj: LLDB variable to compute summary.
        :param dict internal_dict: Internal LLDB dictionary.
        """
        super(CFHTTPMessageContentSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            self.tmp1_offset = 0x30
            self.http_header_dict_offset1 = 0x60
            self.http_header_dict_offset2 = 0x68
            self.http_method_offset = 0x88
        else:
            self.tmp1_offset = 0x18
            self.http_header_dict_offset1 = 0x30
            self.http_header_dict_offset2 = 0x34
            self.http_method_offset = 0x44

        self.register_child_value("tmp1", type_name="void_ptr_type", offset=self.tmp1_offset,
                                  provider_class=CFHTTPMessageContentTempSyntheticProvider)
        self.register_child_value("http_header_dict1", type_name="void_ptr_type", offset=self.http_header_dict_offset1,
                                  provider_class=HTTPHeaderDict.HTTPHeaderDictContentTempSyntheticProvider)
        self.register_child_value("http_header_dict2", type_name="void_ptr_type", offset=self.http_header_dict_offset2,
                                  provider_class=HTTPHeaderDict.HTTPHeaderDictContentTempSyntheticProvider)
        self.register_child_value("http_method", type_name="NSString *", offset=self.http_method_offset,
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_http_method_summary)

    def get_http_header_dict(self):
        """
        Returns http header value (SBValue) which contains headers data.

        :return: Http header value (SBValue) which contains headers data.
        :rtype: lldb.SBValue
        """
        value = SummaryBase.get_signed_value(self.http_header_dict2)
        if value is None or value == 0:
            return self.http_header_dict1
        return self.http_header_dict2

    def get_http_header_dict_provider(self):
        """
        Returns http header provider (HTTPHeaderDict.HTTPHeaderDictContentTempSyntheticProvider) which contains headers data.

        :return: Http header provider (HTTPHeaderDict.HTTPHeaderDictContentTempSyntheticProvider) which contains headers data.
        :rtype: HTTPHeaderDict.HTTPHeaderDictContentTempSyntheticProvider
        """
        value = SummaryBase.get_signed_value(self.http_header_dict2)
        if value is None or value == 0:
            return self.http_header_dict1_provider
        return self.http_header_dict2_provider

    @staticmethod
    def get_http_method_summary(value):
        return value


class CFHTTPMessageContentTempSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing CFHTTPMessage content temp structure.

    :param int http_body_offset: Offset to HTTP body data.
    """
    # struct _tmp1:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSData *HTTPBody                                                        8 = 0x08 / 4           16 = 0x10 / 8

    def __init__(self, value_obj, internal_dict):
        super(CFHTTPMessageContentTempSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            self.http_body_offset = 0x10
        else:
            self.http_body_offset = 0x8

        self.register_child_value("http_body", type_name="NSData *", offset=self.http_body_offset,
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_http_body_summary)

    @staticmethod
    def get_http_body_summary(value):
        return "body={}".format(value)
