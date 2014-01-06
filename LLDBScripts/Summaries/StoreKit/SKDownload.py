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

import lldb
import summary_helpers
import NSObject


class SKDownload_SynthProvider(NSObject.NSObject_SynthProvider):
    # SKDownload:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSString *_contentIdentifier                                            4 = 0x04 / 4            8 = 0x08 / 8
    # long long _contentLength                                                8 = 0x08 / 8           16 = 0x10 / 8
    # NSURL *_contentURL                                                     16 = 0x10 / 4           24 = 0x18 / 8
    # NSNumber *_downloadID                                                  20 = 0x14 / 4           32 = 0x20 / 8
    # NSInteger _downloadState                                               24 = 0x18 / 4           40 = 0x28 / 8
    # NSError *_error                                                        28 = 0x1c / 4           48 = 0x30 / 8
    # float _progress                                                        32 = 0x20 / 4           56 = 0x38 / 4 + 4
    # double _timeRemaining                                                  36 = 0x24 / 8           64 = 0x40 / 8
    # SKPaymentTransaction *_transaction                                     44 = 0x2c / 4           72 = 0x48 / 8
    # NSString *_version                                                     48 = 0x30 / 4           80 = 0x50 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(SKDownload_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.content_identifier = None
        self.content_length = None
        self.content_url = None
        self.download_id = None
        self.download_state = None
        self.progress = None
        self.time_remaining = None
        self.version = None
        
        self.update()

    def update(self):
        self.content_identifier = None
        self.content_length = None
        self.content_url = None
        self.download_id = None
        self.download_state = None
        self.progress = None
        self.time_remaining = None
        self.version = None
        super(SKDownload_SynthProvider, self).update()

    # _contentIdentifier (self->_contentIdentifier)
    def get_content_identifier(self):
        if self.content_identifier:
            return self.content_identifier

        self.content_identifier = self.value_obj.CreateChildAtOffset("contentIdentifier",
                                                                     1 * self.sys_params.pointer_size,
                                                                     self.sys_params.types_cache.NSString)
        return self.content_identifier

    # _contentLength (self->_contentLength)
    def get_content_length(self):
        if self.content_length:
            return self.content_length

        self.content_length = self.value_obj.CreateChildAtOffset("contentLength",
                                                                 2 * self.sys_params.pointer_size,
                                                                 self.sys_params.types_cache.longlong)
        return self.content_length

    # _contentURL (self->_contentURL)
    def get_content_url(self):
        if self.content_url:
            return self.content_url

        if self.sys_params.is_64_bit:
            offset = 3 * self.sys_params.pointer_size
        else:
            offset = 4 * self.sys_params.pointer_size

        self.content_url = self.value_obj.CreateChildAtOffset("contentURL",
                                                              offset,
                                                              self.sys_params.types_cache.longlong)
        return self.content_url

    # _downloadID (self->_downloadID)
    def get_download_id(self):
        if self.download_id:
            return self.download_id

        if self.sys_params.is_64_bit:
            offset = 4 * self.sys_params.pointer_size
        else:
            offset = 5 * self.sys_params.pointer_size

        self.download_id = self.value_obj.CreateChildAtOffset("downloadID",
                                                              offset,
                                                              self.sys_params.types_cache.NSNumber)
        return self.download_id

    # _downloadState (self->_downloadState)
    def get_download_state(self):
        if self.download_state:
            return self.download_state

        if self.sys_params.is_64_bit:
            offset = 5 * self.sys_params.pointer_size
        else:
            offset = 4 * self.sys_params.pointer_size

        self.download_state = self.value_obj.CreateChildAtOffset("downloadState",
                                                                 offset,
                                                                 self.sys_params.types_cache.int)

        return self.download_state

    # _progress (self->_progress)
    def get_progress(self):
        if self.progress:
            return self.progress

        if self.sys_params.is_64_bit:
            offset = 7 * self.sys_params.pointer_size
        else:
            offset = 8 * self.sys_params.pointer_size

        self.progress = self.value_obj.CreateChildAtOffset("progress",
                                                           offset,
                                                           self.sys_params.types_cache.float)

        return self.progress

    # _timeRemaining (self->_timeRemaining)
    def get_time_remaining(self):
        if self.time_remaining:
            return self.time_remaining

        if self.sys_params.is_64_bit:
            offset = 8 * self.sys_params.pointer_size
        else:
            offset = 9 * self.sys_params.pointer_size

        self.time_remaining = self.value_obj.CreateChildAtOffset("timeRemaining",
                                                                 offset,
                                                                 self.sys_params.types_cache.double)

        return self.time_remaining

    # _version (self->_version)
    def get_version(self):
        if self.version:
            return self.version

        if self.sys_params.is_64_bit:
            offset = 10 * self.sys_params.pointer_size
        else:
            offset = 12 * self.sys_params.pointer_size

        self.version = self.value_obj.CreateChildAtOffset("version",
                                                          offset,
                                                          self.sys_params.types_cache.NSString)

        return self.version

    def summary(self):
        content_id = self.get_content_identifier().GetSummary()
        content_length = self.get_content_length().GetValueAsSigned()

        return "{}, length={}".format(content_id, content_length)


def SKDownload_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, SKDownload_SynthProvider)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type summary add -F SKDownload.SKDownload_SummaryProvider \
                            --category StoreKit \
                            SKDownload")
    debugger.HandleCommand("type category enable StoreKit")
