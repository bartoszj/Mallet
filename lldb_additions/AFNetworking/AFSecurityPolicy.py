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

AFSSLPinningModeNone = 0
AFSSLPinningModePublicKey = 1
AFSSLPinningModeCertificate = 2


class AFSecurityPolicySyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing AFSecurityPolicy.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFSecurityPolicySyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("ssl_pinning_mode", ivar_name="_SSLPinningMode",
                                  primitive_value_function=SummaryBase.get_unsigned_value,
                                  summary_function=self.get_ssl_pinning_mode_summary)
        self.register_child_value("validates_certificate_chain", ivar_name="_validatesCertificateChain",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_validates_certificate_chain_summary)
        self.register_child_value("pinned_certificates", ivar_name="_pinnedCertificates",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_pinned_certificates_summary)
        self.register_child_value("pinned_public_keys", ivar_name="_pinnedPublicKeys",
                                  primitive_value_function=SummaryBase.get_count_value,
                                  summary_function=self.get_pinned_public_keys_summary)
        self.register_child_value("allow_invalid_certificates", ivar_name="_allowInvalidCertificates",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_allow_invalid_certificates_summary)
        self.register_child_value("validates_domain_name", ivar_name="_validatesDomainName",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_validates_domain_name_summary)

    @staticmethod
    def get_ssl_pinning_mode_summary(value):
        text = get_ssl_pinning_mode_text(value)
        return "sslPinningMode={}".format(text)

    @staticmethod
    def get_validates_certificate_chain_summary(value):
        if value is False:
            return "notValidatesCertificateChain"
        return None

    @staticmethod
    def get_pinned_certificates_summary(value):
        if value == 0:
            return None
        return "pinnedCertificates={}".format(value)

    @staticmethod
    def get_pinned_public_keys_summary(value):
        if value == 0:
            return None
        return "pinnedPublicKeys={}".format(value)

    @staticmethod
    def get_allow_invalid_certificates_summary(value):
        if value:
            return "allowInvalidCertificates"
        return None

    @staticmethod
    def get_validates_domain_name_summary(value):
        if value is False:
            return "notValidatesDomainName"
        return None

    def summaries_parts(self):
        return [self.allow_invalid_certificates_summary,
                self.validates_certificate_chain_summary,
                self.validates_domain_name_summary,
                self.ssl_pinning_mode_summary,
                self.pinned_certificates_summary,
                self.pinned_public_keys_summary]


def get_ssl_pinning_mode_text(value):
    """
    Returns AFSSLPinningMode value as text.

    :param int value: AFSSLPinningMode value.
    :return: AFSSLPinningMode value as text.
    :rtype: str
    """
    if value == AFSSLPinningModeNone:
        return "None"
    elif value == AFSSLPinningModePublicKey:
        return "PublicKey"
    elif value == AFSSLPinningModeCertificate:
        return "Certificate"
    return "Unknown"


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFSecurityPolicySyntheticProvider)
