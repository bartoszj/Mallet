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
    # UISlider:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # float _value                                                          120 = 0x78 / 4          220 = 0xdc / 4
    # float _minValue                                                       124 = 0x7c / 4          224 = 0xe0 / 4
    # float _maxValue                                                       128 = 0x80 / 4          228 = 0xe4 / 4
    # CGFloat _alpha                                                        132 = 0x84 / 4          232 = 0xe8 / 8
    # struct __CFDictionary *_contentLookup                                 136 = 0x88 / 4          240 = 0xf0 / 8
    # UIImageView *_minValueImageView                                       140 = 0x8c / 4          248 = 0xf8 / 8
    # UIImageView *_maxValueImageView                                       144 = 0x90 / 4          256 = 0x100 / 8
    # UIImageView *_thumbView                                               148 = 0x94 / 4          264 = 0x108 / 8
    # UIImageView *_minTrackView                                            152 = 0x98 / 4          272 = 0x110 / 8
    # UIImageView *_maxTrackView                                            156 = 0x9c / 4          280 = 0x118 / 8
    # UIView *_maxTrackClipView                                             160 = 0xa0 / 4          288 = 0x120 / 8
    # struct {
    #     unsigned int continuous:1;
    #     unsigned int animating:1;
    #     unsigned int preparingToAnimate:1;
    #     unsigned int showValue:1;
    #     unsigned int trackEnabled:1;
    #     unsigned int creatingSnapshot:1;
    #     unsigned int thumbDisabled:1;
    #     unsigned int minTrackHidden:1;
    # } _sliderFlags                                                        164 = 0xa4 / 1 + 3      296 = 0x128 / 8
    # CGFloat _hitOffset                                                    168 = 0xa8 / 4          304 = 0x130 / 8
    # UIColor *_minTintColor                                                172 = 0xac / 4          312 = 0x138 / 8
    # UIColor *_maxTintColor                                                176 = 0xb0 / 4          320 = 0x140 / 8
    # UIColor *_thumbTintColor                                              180 = 0xb4 / 4          328 = 0x148 / 8
    # CAShapeLayer *_trackMaskLayer                                         184 = 0xb8 / 4          336 = 0x150 / 8
    # UIView *_trackContainerView                                           188 = 0xbc / 4          344 = 0x158 / 8
    # UIView *_thumbViewNeue                                                192 = 0xc0 / 4          352 = 0x160 / 8
    # CAShapeLayer *_thumbViewNeueShape                                     196 = 0xc4 / 4          360 = 0x168 / 8
    # BOOL _useLookNeue                                                     200 = 0xc8 / 1          368 = 0x170 / 1
    # BOOL _trackIsArtworkBased                                             201 = 0xc9 / 1          369 = 0x171 / 1
    # BOOL _thumbIsArtworkBased                                             202 = 0xca / 1 + 1      370 = 0x172 / 1 + 5
    # UIView *_minTrackViewNeue                                             204 = 0xcc / 4          376 = 0x178 / 8
    # UIView *_maxTrackViewNeue                                             208 = 0xd0 / 4          384 = 0x180 / 8
    # CAGradientLayer *_maxTrackGradientLayer                               212 = 0xd4 / 4          392 = 0x188 / 8
    # BOOL _maxColorIsValid                                                 216 = 0xd8 / 1 + 3      400 = 0x190 / 1 + 7
    # UIImageView *_innerThumbView                                          220 = 0xdc / 4          408 = 0x198 / 8

    def __init__(self, value_obj, internal_dict):
        super(UISlider_SynthProvider, self).__init__(value_obj, internal_dict)

        self.value = None
        self.min = None
        self.max = None

    def get_value(self):
        if self.value:
            return self.value

        self.value = self.get_child_value("_value")
        return self.value

    def get_min(self):
        if self.min:
            return self.min

        self.min = self.get_child_value("_minValue")
        return self.min

    def get_max(self):
        if self.max:
            return self.max

        self.max = self.get_child_value("_maxValue")
        return self.max

    def summary(self):
        value = self.get_value()
        value_value = float(value.GetValue())
        value_summary = "value={}".format(value_value)

        minimum = self.get_min()
        minimum_value = float(minimum.GetValue())
        minimum_summary = "min={}".format(minimum_value)

        maximum = self.get_max()
        maximum_value = float(maximum.GetValue())
        maximum_summary = "max={}".format(maximum_value)

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
