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
import objc_runtime
import summary_helpers
import UIView

statistics = lldb.formatters.metrics.Metrics()
statistics.add_metric('invalid_isa')
statistics.add_metric('invalid_pointer')
statistics.add_metric('unknown_class')
statistics.add_metric('code_notrun')


class UILabel_SynthProvider(UIView.UIView_SynthProvider):
    # UILabel:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # CGSize _size                                                           96 = 0x60 / 8          184 = 0xb8 / 16
    # UIColor *_highlightedColor                                            104 = 0x68 / 4          200 = 0xc8 / 8
    # NSInteger _numberOfLines                                              108 = 0x6c / 4          208 = 0xd0 / 8
    # NSInteger _measuredNumberOfLines                                      112 = 0x70 / 4          216 = 0xd8 / 8
    # CGFloat _lastLineBaseline                                             116 = 0x74 / 4          224 = 0xe0 / 8
    # CGFloat _minimumScaleFactor                                           120 = 0x78 / 4          232 = 0xe8 / 8
    # NSMutableAttributedString *_attributedText                            124 = 0x7c / 4          240 = 0xf0 / 8
    # NSAttributedString *_synthesizedAttributedText                        128 = 0x80 / 4          248 = 0xf8 / 8
    # NSMutableDictionary *_defaultAttributes                               132 = 0x84 / 4          256 = 0x100 / 8
    # CGFloat _minimumFontSize                                              136 = 0x88 / 4          264 = 0x108 / 8
    # NSInteger _lineSpacing                                                140 = 0x8c / 4          272 = 0x110 / 8
    # id _layout                                                            144 = 0x90 / 4          280 = 0x118 / 8
    # _UILabelScaledMetrics *_scaledMetrics                                 148 = 0x94 / 4          288 = 0x120 / 8
    # struct {
    #     unsigned unused1 : 3;
    #     unsigned highlighted : 1;
    #     unsigned autosizeTextToFit : 1;
    #     unsigned autotrackTextToFit : 1;
    #     unsigned baselineAdjustment : 2;
    #     unsigned unused2 : 2;
    #     unsigned enabled : 1;
    #     unsigned wordRoundingEnabled : 1;
    #     unsigned explicitAlignment : 1;
    #     unsigned marqueeEnabled : 1;
    #     unsigned marqueeRunable : 1;
    #     unsigned marqueeRequired : 1;
    #     unsigned drawsLetterpress : 1;
    #     unsigned unused3 : 1;
    #     unsigned usesExplicitPreferredMaxLayoutWidth : 1;
    #     unsigned determiningPreferredMaxLayoutWidth : 1;
    #     unsigned inSecondConstraintsPass : 1;
    #     unsigned drawsDebugBaselines : 1;
    #     unsigned explicitBaselineOffset : 1;
    #     unsigned usesSimpleTextEffects : 1;
    # } _textLabelFlags                                                     156 = 0x9c / 3 + 1      296 = 0x128 / 3 + 5
    # CGFloat _preferredMaxLayoutWidth                                      160 = 0xa0 / 4          304 = 0x130 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        # Super doesn't work :(
        # self.as_super = super(UILabel_SynthProvider, self)
        # self.as_super.__init__(value_obj, sys_params, internal_dict)
        # super(UILabel_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.value_obj = value_obj
        self.sys_params = sys_params
        self.internal_dict = internal_dict

        self.text = None
        self.update()

    def update(self):
        super(UILabel_SynthProvider, self).update()
        self.adjust_for_architecture()
        self.text = None

    def adjust_for_architecture(self):
        super(UILabel_SynthProvider, self).adjust_for_architecture()
        pass

    def get_text(self):
        if self.text:
            return self.text

        if self.sys_params.is_64_bit:
            offset = 0xf0
        else:
            offset = 0x7c

        self.text = self.value_obj.CreateChildAtOffset("attributedText",
                                                       offset,
                                                       self.sys_params.types_cache.NSAttributedString)
        return self.text

    def summary(self):
        text = self.get_text()
        text_summary = "text={}".format(text.GetSummary())

        return text_summary


def UILabel_SummaryProvider(value_obj, internal_dict):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    if not class_data.is_valid():
        return ""
    summary_helpers.update_sys_params(value_obj, class_data.sys_params)
    if wrapper is not None:
        return wrapper.message()

    wrapper = UILabel_SynthProvider(value_obj, class_data.sys_params, internal_dict)
    if wrapper is not None:
        return wrapper.summary()
    return "Summary Unavailable"


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UILabel.UILabel_SummaryProvider \
                            --category UIKit \
                            UILabel")
    debugger.HandleCommand("type category enable UIKit")
