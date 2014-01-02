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

import lldb
import summary_helpers
import UIView


class UIProgressView_SynthProvider(UIView.UIView_SynthProvider):
    # UIProgressView:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # NSInteger _progressViewStyle                                          96 = 0x60 / 4           184 = 0xb8 / 8
    # float _progress                                                       100 = 0x64 / 4          192 = 0xc0 / 4 + 4
    # NSInteger _barStyle                                                   104 = 0x68 / 4          200 = 0xc8 / 8
    # UIColor *_progressTintColor                                           108 = 0x6c / 4          208 = 0xd0 / 8
    # UIColor *_trackTintColor                                              112 = 0x70 / 4          216 = 0xd8 / 8
    # UIImageView *_trackView                                               116 = 0x74 / 4          224 = 0xe0 / 8
    # UIImageView *_progressView                                            120 = 0x78 / 4          232 = 0xe8 / 8
    # BOOL _isAnimating                                                     124 = 0x7c / 1          240 = 0xf0 / 1
    # BOOL _useArtwork                                                      125 = 0x7d / 1 + 2      241 = 0xf1 / 1 + 6
    # CAGradientLayer *_trackGradientLayer                                  128 = 0x80 / 4          248 = 0xf8 / 8
    # CAGradientLayer *_progressGradientLayer                               132 = 0x84 / 4          256 = 0x100 / 8
    # struct CGRect _previousBounds                                         136 = 0x88 / 16         264 = 0x108 / 32
    # struct CGRect _previousProgressBounds                                 152 = 0x98 / 16         296 = 0x128 / 32
    # UIImage *_trackImage                                                  168 = 0xa8 / 4          328 = 0x148 / 8
    # UIImage *_progressImage                                               172 = 0xac / 4          226 = 0x150 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        # self.as_super = super(UIProgressView_SynthProvider, self)
        # self.as_super.__init__(value_obj, sys_params, internal_dict)
        super(UIProgressView_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.progress = None

        self.update()

    def update(self):
        self.progress = None
        super(UIProgressView_SynthProvider, self).update()

    def adjust_for_architecture(self):
        super(UIProgressView_SynthProvider, self).adjust_for_architecture()

    def get_progress(self):
        if self.progress:
            return self.progress

        if self.sys_params.is_64_bit:
            offset = 0xc0
        else:
            offset = 0x64

        self.progress = self.value_obj.CreateChildAtOffset("progress",
                                                           offset,
                                                           self.sys_params.types_cache.float)
        return self.progress

    def summary(self):
        progress = self.get_progress()
        progress_value = float(progress.GetValue())
        progress_summary = "progress={:.4f}".format(progress_value)

        return progress_summary


def UIProgressView_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIProgressView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIProgressView.UIProgressView_SummaryProvider \
                            --category UIKit \
                            UIProgressView")
    debugger.HandleCommand("type category enable UIKit")
