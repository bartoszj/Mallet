#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
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

import Helpers
import NSObject


class SKDownload_SynthProvider(NSObject.NSObject_SynthProvider):
    # Class: SKDownload
    # Super class: NSObject
    # Name:                                   armv7                 i386                  arm64                 x86_64
    # NSString * _contentIdentifier         4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # long long _contentLength              8 (0x008) / 8         8 (0x008) / 8        16 (0x010) / 8        16 (0x010) / 8
    # NSURL * _contentURL                  16 (0x010) / 4        16 (0x010) / 4        24 (0x018) / 8        24 (0x018) / 8
    # NSNumber * _downloadID               20 (0x014) / 4        20 (0x014) / 4        32 (0x020) / 8        32 (0x020) / 8
    # NSInteger _downloadState             24 (0x018) / 4        24 (0x018) / 4        40 (0x028) / 8        40 (0x028) / 8
    # NSError * _error                     28 (0x01C) / 4        28 (0x01C) / 4        48 (0x030) / 8        48 (0x030) / 8
    # float _progress                      32 (0x020) / 4        32 (0x020) / 4        56 (0x038) / 4  + 4   56 (0x038) / 4  + 4
    # double _timeRemaining                36 (0x024) / 8        36 (0x024) / 8        64 (0x040) / 8        64 (0x040) / 8
    # SKPaymentTransaction * _transaction  44 (0x02C) / 4        44 (0x02C) / 4        72 (0x048) / 8        72 (0x048) / 8
    # NSString * _version                  48 (0x030) / 4        48 (0x030) / 4        80 (0x050) / 8        80 (0x050) / 8

    def __init__(self, value_obj, internal_dict):
        super(SKDownload_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "SKDownload"

        self.content_identifier = None
        self.content_length = None
        self.content_url = None
        self.download_id = None
        self.download_state = None
        self.progress = None
        self.time_remaining = None
        self.version = None

    def get_content_identifier(self):
        if self.content_identifier:
            return self.content_identifier

        self.content_identifier = self.get_child_value("_contentIdentifier")
        return self.content_identifier

    def get_content_length(self):
        if self.content_length:
            return self.content_length

        self.content_length = self.get_child_value("_contentLength")
        return self.content_length

    def get_content_url(self):
        if self.content_url:
            return self.content_url

        self.content_url = self.get_child_value("_contentURL")
        return self.content_url

    def get_download_id(self):
        if self.download_id:
            return self.download_id

        self.download_id = self.get_child_value("_downloadID")
        return self.download_id

    def get_download_state(self):
        if self.download_state:
            return self.download_state

        self.download_state = self.get_child_value("_downloadState")
        return self.download_state

    def get_progress(self):
        if self.progress:
            return self.progress

        self.progress = self.get_child_value("_progress")
        return self.progress

    def get_time_remaining(self):
        if self.time_remaining:
            return self.time_remaining

        self.time_remaining = self.get_child_value("_timeRemaining")
        return self.time_remaining

    def get_version(self):
        if self.version:
            return self.version

        self.version = self.get_child_value("_version")
        return self.version

    def summary(self):
        content_id = self.get_content_identifier().GetSummary()
        content_length = self.get_content_length().GetValueAsSigned()

        return "{}, length={}".format(content_id, content_length)


def SKDownload_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, SKDownload_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKDownload.SKDownload_SummaryProvider \
                            --category StoreKit \
                            SKDownload")
    debugger.HandleCommand("type category enable StoreKit")
