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
import UIView


class UILabel_SynthProvider(UIView.UIView_SynthProvider):
    # UILabel:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
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

    def __init__(self, value_obj, internal_dict):
        super(UILabel_SynthProvider, self).__init__(value_obj, internal_dict)

        self.text = None

    def get_text(self):
        if self.text:
            return self.text

        self.text = self.get_child_value("_content", "NSMutableAttributedString *")
        return self.text

    def summary(self):
        text = self.get_text()
        text_summary = "text={}".format(text.GetSummary())

        return text_summary


def UILabel_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UILabel_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UILabel.UILabel_SummaryProvider \
                            --category UIKit \
                            UILabel")
    debugger.HandleCommand("type category enable UIKit")
