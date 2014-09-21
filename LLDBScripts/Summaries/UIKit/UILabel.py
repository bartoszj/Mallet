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
    # Class: UILabel
    # Super class: UIView
    # Protocols: NSCoding
    # Name:                                                           armv7                 i386                  arm64                 x86_64
    # CGSize _size                                                 96 (0x060) / 8        96 (0x060) / 8       184 (0x0B8) / 16      184 (0x0B8) / 16
    # UIColor * _highlightedColor                                 104 (0x068) / 4       104 (0x068) / 4       200 (0x0C8) / 8       200 (0x0C8) / 8
    # NSInteger _numberOfLines                                    108 (0x06C) / 4       108 (0x06C) / 4       208 (0x0D0) / 8       208 (0x0D0) / 8
    # NSInteger _measuredNumberOfLines                            112 (0x070) / 4       112 (0x070) / 4       216 (0x0D8) / 8       216 (0x0D8) / 8
    # CGFloat _lastLineBaseline                                   116 (0x074) / 4       116 (0x074) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # CGFloat _minimumScaleFactor                                 120 (0x078) / 4       120 (0x078) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # id _content                                                 124 (0x07C) / 4       124 (0x07C) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # NSAttributedString * _synthesizedAttributedText             128 (0x080) / 4       128 (0x080) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # NSMutableDictionary * _defaultAttributes                    132 (0x084) / 4       132 (0x084) / 4       256 (0x100) / 8       256 (0x100) / 8
    # CGFloat _minimumFontSize                                    136 (0x088) / 4       136 (0x088) / 4       264 (0x108) / 8       264 (0x108) / 8
    # NSInteger _lineSpacing                                      140 (0x08C) / 4       140 (0x08C) / 4       272 (0x110) / 8       272 (0x110) / 8
    # id _layout                                                  144 (0x090) / 4       144 (0x090) / 4       280 (0x118) / 8       280 (0x118) / 8
    # _UILabelScaledMetrics * _scaledMetrics                      148 (0x094) / 4       148 (0x094) / 4       288 (0x120) / 8       288 (0x120) / 8
    # struct {
    #         unsigned int unused1:3;
    #         unsigned int highlighted:1;
    #         unsigned int autosizeTextToFit:1;
    #         unsigned int autotrackTextToFit:1;
    #         unsigned int baselineAdjustment:2;
    #         unsigned int unused2:2;
    #         unsigned int enabled:1;
    #         unsigned int wordRoundingEnabled:1;
    #         unsigned int explicitAlignment:1;
    #         unsigned int marqueeEnabled:1;
    #         unsigned int marqueeRunable:1;
    #         unsigned int marqueeRequired:1;
    #         unsigned int drawsLetterpress:1;
    #         unsigned int unused3:1;
    #         unsigned int usesExplicitPreferredMaxLayoutWidth:1;
    #         unsigned int determiningPreferredMaxLayoutWidth:1;
    #         unsigned int inSecondConstraintsPass:1;
    #         unsigned int drawsDebugBaselines:1;
    #         unsigned int explicitBaselineOffset:1;
    #         unsigned int usesSimpleTextEffects:1;
    #         unsigned int isComplexString:1;
    #     } _textLabelFlags                                       152 (0x098) / 4       152 (0x098) / 4       296 (0x128) / 4       296 (0x128) / 4
    # BOOL _wantsUnderlineForAccessibilityButtonShapesEnabled     156 (0x09C) / 1  + 3  156 (0x09C) / 1  + 3  300 (0x12C) / 1  + 3  300 (0x12C) / 1  + 3
    # CGFloat _preferredMaxLayoutWidth                            160 (0x0A0) / 4       160 (0x0A0) / 4       304 (0x130) / 8       304 (0x130) / 8

    def __init__(self, value_obj, internal_dict):
        super(UILabel_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UILabel"

        self.text = None

    @Helpers.save_parameter("text")
    def get_text(self):
        return self.get_child_value("_content", "NSAttributedString *")

    def get_text_value(self):
        return self.get_summary_value(self.get_text())

    def get_text_summary(self):
        text_value = self.get_text_value()
        return None if text_value is None else "text={}".format(text_value)

    def summary(self):
        text_summary = self.get_text_summary()
        tag_summary = self.get_tag_summary()

        summaries = []
        if text_summary:
            summaries.append(text_summary)
        if self.get_tag_value() != 0:
            summaries.append(tag_summary)

        summary = ", ".join(summaries)
        return summary


def UILabel_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UILabel_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UILabel.UILabel_SummaryProvider \
                            --category UIKit \
                            UILabel")
    debugger.HandleCommand("type category enable UIKit")
