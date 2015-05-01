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
from .. import SummaryBase
from ..Foundation import NSObject
import NSURLRequest
import NSHTTPCookieStorage

kSSLProtocolUnknown = 0
kSSLProtocol3 = 2
kTLSProtocol1 = 4
kTLSProtocol11 = 7
kTLSProtocol12 = 8
kDTLSProtocol1 = 9

# Deprecated
kSSLProtocol2 = 1
kSSLProtocol3Only = 3
kTLSProtocol1Only = 5
kSSLProtocolAll = 6


class NSURLSessionConfigurationSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSURLSessionConfiguration.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSURLSessionConfigurationSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSURLSessionConfiguration"

        self.register_child_value("allows_cellular_access", ivar_name="_allowsCellularAccess",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_allows_cellular_access_summary)
        self.register_child_value("discretionary", ivar_name="_discretionary",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_discretionary_summary)
        self.register_child_value("session_sends_launch_events", ivar_name="_sessionSendsLaunchEvents",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_session_sends_launch_events_summary)
        self.register_child_value("http_should_use_pipelining", ivar_name="_HTTPShouldUsePipelining",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_http_should_use_pipelining_summary)
        self.register_child_value("http_should_set_cookies", ivar_name="_HTTPShouldSetCookies",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_http_should_set_cookies_summary)
        self.register_child_value("background_session", ivar_name="_backgroundSession",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_background_session_summary)
        self.register_child_value("disallows_spdy", ivar_name="__disallowsSPDY",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_disallows_spdy_summary)
        self.register_child_value("tls_minimum_supported_protocol", ivar_name="_TLSMinimumSupportedProtocol",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_tls_minimum_supported_protocol_summary)
        self.register_child_value("tls_maximum_supported_protocol", ivar_name="_TLSMaximumSupportedProtocol",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_tls_maximum_supported_protocol_summary)
        self.register_child_value("identifier", ivar_name="_identifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_identifier_summary)
        self.register_child_value("request_cache_policy", ivar_name="_requestCachePolicy",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_request_cache_policy_summary)
        self.register_child_value("timeout_interval_for_request", ivar_name="_timeoutIntervalForRequest",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_timeout_interval_for_request_summary)
        self.register_child_value("timeout_interval_for_resource", ivar_name="_timeoutIntervalForResource",
                                  primitive_value_function=SummaryBase.get_float_value,
                                  summary_function=self.get_timeout_interval_for_resource_summary)
        self.register_child_value("network_service_type", ivar_name="_networkServiceType",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_network_service_type_summary)
        self.register_child_value("shared_container_identifier", ivar_name="_sharedContainerIdentifier",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_shared_container_identifier_summary)
        self.register_child_value("http_cookie_accept_policy", ivar_name="_HTTPCookieAcceptPolicy",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_http_cookie_accept_policy_summary)
        self.register_child_value("http_additional_headers", ivar_name="_HTTPAdditionalHeaders",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_http_additional_headers_summary)
        self.register_child_value("http_maximum_connections_per_host", ivar_name="_HTTPMaximumConnectionsPerHost",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_http_maximum_connections_per_host_summary)
        self.register_child_value("protocol_classes", ivar_name="_protocolClasses",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_protocol_classes_summary)

    @staticmethod
    def get_allows_cellular_access_summary(value):
        if not value:
            return "disallowsCellularAccess"
        return None

    @staticmethod
    def get_discretionary_summary(value):
        if value:
            return "discretionary"
        return None

    @staticmethod
    def get_session_sends_launch_events_summary(value):
        if value:
            return "sessionSendsLaunchEvents"
        return None

    @staticmethod
    def get_http_should_use_pipelining_summary(value):
        if value:
            return "shouldUsePipelining"
        return None

    @staticmethod
    def get_http_should_set_cookies_summary(value):
        if not value:
            return "dontSetCookies"
        return None

    @staticmethod
    def get_background_session_summary(value):
        if value:
            return "backgroundSession"
        return None

    @staticmethod
    def get_disallows_spdy_summary(value):
        if value:
            return "disallowsSPDY"
        return None

    @staticmethod
    def get_tls_minimum_supported_protocol_summary(value):
        if value == kSSLProtocol3:
            return None
        tls = get_tls_version_text(value)
        return "TLSMin={}".format(tls)

    @staticmethod
    def get_tls_maximum_supported_protocol_summary(value):
        if value == kTLSProtocol12:
            return None
        tls = get_tls_version_text(value)
        return "TLSMax={}".format(tls)

    @staticmethod
    def get_identifier_summary(value):
        return "identifier={}".format(value)

    @staticmethod
    def get_request_cache_policy_summary(value):
        if value == NSURLRequest.NSURLRequestUseProtocolCachePolicy:
            return None
        cache_policy = NSURLRequest.get_cache_policy_text(value)
        return "cachePolicy={}".format(cache_policy)

    @staticmethod
    def get_timeout_interval_for_request_summary(value):
        if value != 60.0:
            return "timeoutRequest={}".format(SummaryBase.formatted_float(value))
        return None

    @staticmethod
    def get_timeout_interval_for_resource_summary(value):
        if value != 604800.0:
            return "timeoutResource={}".format(SummaryBase.formatted_float(value))
        return None

    @staticmethod
    def get_network_service_type_summary(value):
        if value == NSURLRequest.NSURLNetworkServiceTypeDefault:
            return None
        service_type = NSURLRequest.get_network_service_type_text(value)
        return "networkServiceType={}".format(service_type)

    @staticmethod
    def get_shared_container_identifier_summary(value):
        return "sharedContainerIdentifier={}".format(value)

    @staticmethod
    def get_http_cookie_accept_policy_summary(value):
        if value == NSHTTPCookieStorage.NSHTTPCookieAcceptPolicyOnlyFromMainDocumentDomain:
            return None
        accept_policy = NSHTTPCookieStorage.get_http_cookie_accept_policy(value)
        return "HTTPCookieAcceptPolicy={}".format(accept_policy)

    @staticmethod
    def get_http_additional_headers_summary(value):
        return "HTTPAdditionalHeaders={}".format(value)

    @staticmethod
    def get_http_maximum_connections_per_host_summary(value):
        if value != 4:
            return "HTTPMaximumConnectionsPerHost={}".format(value)
        return None

    @staticmethod
    def get_protocol_classes_summary(value):
        return "protocolClasses={}".format(value)

    def summaries_parts(self):
        return [self.identifier_summary,
                self.shared_container_identifier_summary,
                self.allows_cellular_access_summary,
                self.discretionary_summary,
                self.session_sends_launch_events_summary,
                self.http_should_use_pipelining_summary,
                self.http_should_set_cookies_summary,
                self.background_session_summary,
                self.disallows_spdy_summary,
                self.tls_minimum_supported_protocol_summary,
                self.tls_maximum_supported_protocol_summary,
                self.request_cache_policy_summary,
                self.timeout_interval_for_request_summary,
                self.timeout_interval_for_resource_summary,
                self.network_service_type_summary,
                self.http_cookie_accept_policy_summary,
                # self.http_additional_headers_summary,
                self.http_maximum_connections_per_host_summary,
                # self.protocol_classes_summary
                ]


def get_tls_version_text(value):
    if value == kSSLProtocolUnknown:
        return "Unknown"
    elif value == kSSLProtocol2:
        return "SSLv2"
    elif value == kSSLProtocol3:
        return "SSLv3"
    elif value == kSSLProtocol3Only:
        return "SSL3_only"
    elif value == kTLSProtocol1:
        return "TLSv1"
    elif value == kTLSProtocol1Only:
        return "TSLv1_only"
    elif value == kSSLProtocolAll:
        return "SSL_all"
    elif value == kTLSProtocol11:
        return "TLSv1.1"
    elif value == kTLSProtocol12:
        return "TLSv1.2"
    elif value == kDTLSProtocol1:
        return "DTLSv1"
    return "Unknown({})".format(value)


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSURLSessionConfigurationSyntheticProvider)
