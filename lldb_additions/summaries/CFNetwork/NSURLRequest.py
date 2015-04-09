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
from ..Foundation import NSObject
import NSURLRequestInternal

NSURLRequestUseProtocolCachePolicy = 0
NSURLRequestReloadIgnoringLocalCacheData = 1
NSURLRequestReturnCacheDataElseLoad = 2
NSURLRequestReturnCacheDataDontLoad = 3

NSURLNetworkServiceTypeDefault = 0
NSURLNetworkServiceTypeVoIP = 1
NSURLNetworkServiceTypeVideo = 2
NSURLNetworkServiceTypeBackground = 3
NSURLNetworkServiceTypeVoice = 4


class NSURLRequestSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSURLRequest.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSURLRequestSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSURLRequest"

        self.register_child_value("request_internal", ivar_name="_internal",
                                  provider_class=NSURLRequestInternal.NSURLRequestInternalSyntheticProvider,
                                  summary_function=self.get_request_internal_summary)

        self.synthetic_type = self.SYNTHETIC_PROXY_VALUE
        self.synthetic_proxy_value = self.get_proxy_value()

    @staticmethod
    def get_request_internal_summary(provider):
        """
        :param NSURLRequestInternal.NSURLRequestInternalSyntheticProvider provider: NSURLRequestInternal provider.
        """
        return provider.summary()

    def get_proxy_value(self):
        """
        Returns proxy value.

        :return: Proxy value.
        :rtype: lldb.SBValue
        """
        request_internal = self.request_internal_provider
        """:type: NSURLRequestInternal.NSURLRequestInternalSyntheticProvider"""
        request = request_internal.request_provider
        """:type: CFURLResponse.CFURLResponseSyntheticProvider"""
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
        return self.request_internal_summary


def get_cache_policy_text(value):
    if value == NSURLRequestUseProtocolCachePolicy:
        return "UseProtocol"
    elif value == NSURLRequestReloadIgnoringLocalCacheData:
        return "ReloadIgnoringLocalCacheData"
    elif value == NSURLRequestReturnCacheDataElseLoad:
        return "ReturnCacheDataElseLoad"
    elif value == NSURLRequestReturnCacheDataDontLoad:
        return "ReturnCacheDataDontLoad"
    return "Unknown"


def get_network_service_type_text(value):
    if value == NSURLNetworkServiceTypeDefault:
        return "Default"
    elif value == NSURLNetworkServiceTypeVoIP:
        return "VoIP"
    elif value == NSURLNetworkServiceTypeVideo:
        return "Video"
    elif value == NSURLNetworkServiceTypeBackground:
        return "Background"
    elif value == NSURLNetworkServiceTypeVoice:
        return "Voice"
    return "Unknown"


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSURLRequestSyntheticProvider)


def lldb_init(debugger, dictionary):
    debugger.HandleCommand("type summary add -F {}.summary_provider \
                            --category CFNetwork \
                            NSURLRequest NSMutableURLRequest".format(__name__))
    debugger.HandleCommand("type synthetic add -l {}.NSURLRequestSyntheticProvider \
                           --category CFNetwork \
                           NSURLRequest NSMutableURLRequest".format(__name__))
    debugger.HandleCommand("type category enable CFNetwork")
