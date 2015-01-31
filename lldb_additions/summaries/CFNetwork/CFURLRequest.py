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
    Class representing _CFURLRequest structure.

    :param int url_offset: Offset to HTTP url.
    :param int tmp1_offset: Offset to "structure _tmp1"
    :param int tmp2_offset: Offset to "structure _tmp2"
    :param int tmp3_offset: Offset to "structure _tmp3"
    :param int http_method_offset: Offset to HTTP method.
    :param int http_body_offset: Offset to HTTP body data.
    :param int http_headers_offset: Offset to HTTP headers.
    """
    # _CFURLRequest:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSURL *url                                                             20 = 0x14 / 4           40 = 0x28 / 8
    # struct _tmp1 *tmp1                                                     48 = 0x30 / 4           88 = 0x58 / 8

    # struct _tmp1 {
    #     struct _tmp2 *tmp2                                                 24 = 0x18 / 4           48 = 0x30 / 8
    #     struct _tmp3 *tmp3                                                                         96 = 0x60 / 8
    #                                                                                               104 = 0x68 / 8
    #     NSString *HTTPMethod                                               68 = 0x44 / 4          136 = 0x88 / 8
    # }

    # struct _tmp2 {
    #     NSData *HTTPBody                                                    8 = 0x08 / 4           16 = 0x10 / 8
    # }

    # struct _tmp3 {
    #     NSDictionary *allHTTPHeaderFields                                                           8 = 0x08 / 8
    # }

    def __init__(self, value_obj, internal_dict):
        """
        :param lldb.SBValue value_obj: LLDB variable to compute summary.
        :param dict internal_dict: Internal LLDB dictionary.
        """
        super(CFURLRequestSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            self.url_offset = 0x28
            self.tmp1_offset = 0x58
            self.tmp2_offset = 0x30
            self.tmp3_offset = 0x60
            self.http_method_offset = 0x88
            self.http_body_offset = 0x10
            self.http_headers_offset = 0x08
        else:
            self.url_offset = 0x14
            self.tmp1_offset = 0x30
            self.tmp2_offset = 0x18
            self.tmp3_offset = 0x60 #?
            self.http_method_offset = 0x44
            self.http_body_offset = 0x8
            self.http_headers_offset = 0x08 #?

        self.register_child_value("url", type_name="NSURL *", offset=self.url_offset,
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_url_summary)
        self.register_child_value("tmp1", type_name="addr_ptr_type", offset=self.tmp1_offset)

        self.http_method = None
        self.tmp2 = None
        self.tmp3 = None
        self.http_body = None
        self.http_headers = None

    @staticmethod
    def get_url_summary(value):
        return "{}".format(value)

    @helpers.save_parameter("tmp2")
    def get_tmp2(self):
        if self.tmp1 is None:
            return None

        tmp2 = self.tmp1.CreateChildAtOffset("tmp2", self.tmp2_offset, self.get_type("addr_ptr_type"))
        return tmp2

    @helpers.save_parameter("tmp3")
    def get_tmp3(self):
        if self.tmp1 is None:
            return None

        tmp3 = self.tmp1.CreateChildAtOffset("tmp3", self.tmp3_offset, self.get_type("addr_ptr_type"))
        return tmp3

    @helpers.save_parameter("http_method")
    def get_http_method(self):
        if self.tmp1 is None:
            return None
        return self.tmp1.CreateChildAtOffset("HTTPMethod", self.http_method_offset, self.get_type("NSString *"))

    def get_http_method_value(self):
        return SummaryBase.get_stripped_summary_value(self.get_http_method())

    def get_http_method_summary(self):
        method_value = self.get_http_method_value()
        return None if method_value is None else "{}".format(method_value)

    @helpers.save_parameter("http_body")
    def get_http_body(self):
        tmp2 = self.get_tmp2()
        if tmp2 is None:
            return None

        http_body = tmp2.CreateChildAtOffset("HTTPBody", self.http_body_offset, self.get_type("NSData *"))
        return http_body

    def get_http_body_value(self):
        return SummaryBase.get_summary_value(self.get_http_body())

    def get_http_body_summary(self):
        value = self.get_http_body_value()
        return None if value is None else "body={}".format(value)

    @helpers.save_parameter("http_headers")
    def get_http_headers(self):
        tmp3 = self.get_tmp3()
        if tmp3 is None:
            return None

        http_headers = tmp3.CreateChildAtOffset("allHTTPHeaderFields", self.http_headers_offset, self.get_type("NSDictionary *"))
        return http_headers

    def get_http_headers_value(self):
        return SummaryBase.get_count_value(self.get_http_headers())

    def get_http_headers_summary(self):
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
