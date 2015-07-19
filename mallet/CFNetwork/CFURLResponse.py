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
import CFHTTPMessage


class CFURLResponseSyntheticProvider(SummaryBase.SummaryBaseSyntheticProvider):
    """
    Class representing CFURLResponse structure.

    :param int url_offset: Offset to HTTP url.
    :param int http_message_content_offset: Offset to CFHTTPMessageRef content.
    """
    # CFURLResponse:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSURL *url                                                             16 = 0x10 / 4           32 = 0x20 / 8
    # CFHTTPMessageRef http_message_content                                  68 = 0x44 / 4          113 = 0x70 / 8

    def __init__(self, value_obj, internal_dict):
        """
        :param lldb.SBValue value_obj: LLDB variable to compute summary.
        :param dict internal_dict: Internal LLDB dictionary.
        """
        super(CFURLResponseSyntheticProvider, self).__init__(value_obj, internal_dict)

        if self.is_64bit:
            self.url_offset = 0x20
            self.http_message_content_offset = 0x70
        else:
            self.url_offset = 0x10
            self.http_message_content_offset = 0x44

        self.register_child_value("url", type_name="NSURL *", offset=self.url_offset,
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_url_summary)
        self.register_child_value("http_message_content", type_name="void_ptr_type", offset=self.http_message_content_offset,
                                  provider_class=CFHTTPMessage.CFHTTPMessageContentSyntheticProvider)

    @staticmethod
    def get_url_summary(value):
        """
        Returns URL summary.

        :param str value: URL value.
        :return: URL summary.
        :rtype: str
        """
        return "{}".format(value)

    def summaries_parts(self):
        return [self.url_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, CFURLResponseSyntheticProvider)
