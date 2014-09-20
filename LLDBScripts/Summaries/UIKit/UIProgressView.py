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

import Helpers
import UIView


class UIProgressView_SynthProvider(UIView.UIView_SynthProvider):
    # Class: UIProgressView
    # Super class: UIView
    # Protocols: NSCoding
    # Name:                            armv7                 i386                  arm64                 x86_64
    # NSInteger _progressViewStyle  96 (0x060) / 4        96 (0x060) / 4       184 (0x0B8) / 8       184 (0x0B8) / 8
    # float _progress              100 (0x064) / 4       100 (0x064) / 4       192 (0x0C0) / 4  + 4  192 (0x0C0) / 4  + 4
    # NSInteger _barStyle          104 (0x068) / 4       104 (0x068) / 4       200 (0x0C8) / 8       200 (0x0C8) / 8
    # UIColor * _progressTintColor 108 (0x06C) / 4       108 (0x06C) / 4       208 (0x0D0) / 8       208 (0x0D0) / 8
    # UIColor * _trackTintColor    112 (0x070) / 4       112 (0x070) / 4       216 (0x0D8) / 8       216 (0x0D8) / 8
    # UIImageView * _trackView     116 (0x074) / 4       116 (0x074) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # UIImageView * _progressView  120 (0x078) / 4       120 (0x078) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # BOOL _isAnimating            124 (0x07C) / 1  + 3  124 (0x07C) / 1  + 3  240 (0x0F0) / 1  + 7  240 (0x0F0) / 1  + 7
    # NSArray * _trackColors       128 (0x080) / 4       128 (0x080) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # NSArray * _progressColors    132 (0x084) / 4       132 (0x084) / 4       256 (0x100) / 8       256 (0x100) / 8
    # UIImage * _trackImage        136 (0x088) / 4       136 (0x088) / 4       264 (0x108) / 8       264 (0x108) / 8
    # UIImage * _progressImage     140 (0x08C) / 4       140 (0x08C) / 4       272 (0x110) / 8       272 (0x110) / 8

    def __init__(self, value_obj, internal_dict):
        super(UIProgressView_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIProgressView"

        self.progress = None

    def get_progress(self):
        if self.progress:
            return self.progress

        self.progress = self.get_child_value("_progress")
        return self.progress

    def get_progress_value(self):
        return self.get_float_value(self.get_progress())

    def get_progress_summary(self):
        progress_value = self.get_progress_value()
        if progress_value is None:
            return None
        return "progress={}".format(self.formatted_float(progress_value))

    def summary(self):
        progress_summary = self.get_progress_summary()

        return progress_summary


def UIProgressView_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIProgressView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIProgressView.UIProgressView_SummaryProvider \
                            --category UIKit \
                            UIProgressView")
    debugger.HandleCommand("type category enable UIKit")
