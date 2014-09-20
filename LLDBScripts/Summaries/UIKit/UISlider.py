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
import UIControl


class UISlider_SynthProvider(UIControl.UIControl_SynthProvider):
    # Class: UISlider
    # Super class: UIControl
    # Protocols: NSCoding
    # Name:                                          armv7                 i386                  arm64                 x86_64
    # float _value                               120 (0x078) / 4       120 (0x078) / 4       220 (0x0DC) / 4       220 (0x0DC) / 4
    # float _minValue                            124 (0x07C) / 4       124 (0x07C) / 4       224 (0x0E0) / 4       224 (0x0E0) / 4
    # float _maxValue                            128 (0x080) / 4       128 (0x080) / 4       228 (0x0E4) / 4       228 (0x0E4) / 4
    # CGFloat _alpha                             132 (0x084) / 4       132 (0x084) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # NSDictionary * _contentLookup              136 (0x088) / 4       136 (0x088) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # UIImageView * _minValueImageView           140 (0x08C) / 4       140 (0x08C) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # UIImageView * _maxValueImageView           144 (0x090) / 4       144 (0x090) / 4       256 (0x100) / 8       256 (0x100) / 8
    # UIImageView * _thumbView                   148 (0x094) / 4       148 (0x094) / 4       264 (0x108) / 8       264 (0x108) / 8
    # UIImageView * _minTrackView                152 (0x098) / 4       152 (0x098) / 4       272 (0x110) / 8       272 (0x110) / 8
    # UIImageView * _maxTrackView                156 (0x09C) / 4       156 (0x09C) / 4       280 (0x118) / 8       280 (0x118) / 8
    # UIView * _maxTrackClipView                 160 (0x0A0) / 4       160 (0x0A0) / 4       288 (0x120) / 8       288 (0x120) / 8
    # struct {
    #         unsigned int continuous:1;
    #         unsigned int animating:1;
    #         unsigned int preparingToAnimate:1;
    #         unsigned int showValue:1;
    #         unsigned int trackEnabled:1;
    #         unsigned int creatingSnapshot:1;
    #         unsigned int thumbDisabled:1;
    #         unsigned int minTrackHidden:1;
    #     } _sliderFlags                         164 (0x0A4) / 1  + 3  164 (0x0A4) / 4       296 (0x128) / 4  + 4  296 (0x128) / 4  + 4
    # CGFloat _hitOffset                         168 (0x0A8) / 4       168 (0x0A8) / 4       304 (0x130) / 8       304 (0x130) / 8
    # UIColor * _minTintColor                    172 (0x0AC) / 4       172 (0x0AC) / 4       312 (0x138) / 8       312 (0x138) / 8
    # UIColor * _maxTintColor                    176 (0x0B0) / 4       176 (0x0B0) / 4       320 (0x140) / 8       320 (0x140) / 8
    # UIColor * _thumbTintColor                  180 (0x0B4) / 4       180 (0x0B4) / 4       328 (0x148) / 8       328 (0x148) / 8
    # UIView * _thumbViewNeue                    184 (0x0B8) / 4       184 (0x0B8) / 4       336 (0x150) / 8       336 (0x150) / 8
    # CAShapeLayer * _thumbViewNeueShape         188 (0x0BC) / 4       188 (0x0BC) / 4       344 (0x158) / 8       344 (0x158) / 8
    # BOOL _useLookNeue                          192 (0x0C0) / 1  + 3  192 (0x0C0) / 1  + 3  352 (0x160) / 1  + 7  352 (0x160) / 1  + 7
    # NSArray * _trackColors                     196 (0x0C4) / 4       196 (0x0C4) / 4       360 (0x168) / 8       360 (0x168) / 8
    # BOOL _trackIsArtworkBased                  200 (0x0C8) / 1       200 (0x0C8) / 1       368 (0x170) / 1       368 (0x170) / 1
    # BOOL _thumbIsArtworkBased                  201 (0x0C9) / 1       201 (0x0C9) / 1       369 (0x171) / 1       369 (0x171) / 1
    # BOOL _maxColorIsValid                      202 (0x0CA) / 1       202 (0x0CA) / 1       370 (0x172) / 1       370 (0x172) / 1
    # BOOL _animatingWithDynamics                203 (0x0CB) / 1       203 (0x0CB) / 1       371 (0x173) / 1  + 4  371 (0x173) / 1  + 4
    # UIImageView * _innerThumbView              204 (0x0CC) / 4       204 (0x0CC) / 4       376 (0x178) / 8       376 (0x178) / 8

    def __init__(self, value_obj, internal_dict):
        super(UISlider_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UISlider"

        self.value = None
        self.min = None
        self.max = None

    def get_value(self):
        if self.value:
            return self.value

        self.value = self.get_child_value("_value")
        return self.value

    def get_value_value(self):
        return self.get_float_value(self.get_value())

    def get_value_summary(self):
        value_value = self.get_value_value()
        if value_value is None:
            return None
        return "value={}".format(self.formatted_float(value_value))

    def get_min(self):
        if self.min:
            return self.min

        self.min = self.get_child_value("_minValue")
        return self.min

    def get_min_value(self):
        return self.get_float_value(self.get_min())

    def get_min_summary(self):
        minimum_value = self.get_min_value()
        if minimum_value is None:
            return None
        return "min={}".format(self.formatted_float(minimum_value))

    def get_max(self):
        if self.max:
            return self.max

        self.max = self.get_child_value("_maxValue")
        return self.max

    def get_max_value(self):
        return self.get_float_value(self.get_max())

    def get_max_summary(self):
        maximum_value = self.get_max_value()
        if maximum_value is None:
            return maximum_value
        return "max={}".format(self.formatted_float(maximum_value))

    def summary(self):
        value_summary = self.get_value_summary()
        minimum_summary = self.get_min_summary()
        maximum_summary = self.get_max_summary()

        # Summaries
        summaries = [value_summary, minimum_summary, maximum_summary]

        summary = ", ".join(summaries)
        return summary


def UISlider_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UISlider_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UISlider.UISlider_SummaryProvider \
                            --category UIKit \
                            UISlider")
    debugger.HandleCommand("type category enable UIKit")
