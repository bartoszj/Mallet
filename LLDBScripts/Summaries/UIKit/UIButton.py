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
import UIControl
import UILabel


class UIButton_SynthProvider(UIControl.UIControl_SynthProvider):
    # Class: UIButton
    # Super class: UIControl
    # Protocols: NSCoding
    # Name:                                                          armv7                 i386                  arm64                 x86_64
    # NSUInteger _externalFlatEdge                               120 (0x078) / 4       120 (0x078) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # NSDictionary * _contentLookup                              124 (0x07C) / 4       124 (0x07C) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # UIEdgeInsets _contentEdgeInsets                            128 (0x080) / 16      128 (0x080) / 16      240 (0x0F0) / 32      240 (0x0F0) / 32
    # UIEdgeInsets _titleEdgeInsets                              144 (0x090) / 16      144 (0x090) / 16      272 (0x110) / 32      272 (0x110) / 32
    # UIEdgeInsets _imageEdgeInsets                              160 (0x0A0) / 16      160 (0x0A0) / 16      304 (0x130) / 32      304 (0x130) / 32
    # UIImageView * _backgroundView                              176 (0x0B0) / 4       176 (0x0B0) / 4       336 (0x150) / 8       336 (0x150) / 8
    # UIImageView * _imageView                                   180 (0x0B4) / 4       180 (0x0B4) / 4       344 (0x158) / 8       344 (0x158) / 8
    # UILabel * _titleView                                       184 (0x0B8) / 4       184 (0x0B8) / 4       352 (0x160) / 8       352 (0x160) / 8
    # BOOL _initialized                                          188 (0x0BC) / 1  + 3  188 (0x0BC) / 1  + 3  360 (0x168) / 1  + 7  360 (0x168) / 1  + 7
    # NSUInteger _lastDrawingControlState                        192 (0x0C0) / 4       192 (0x0C0) / 4       368 (0x170) / 8       368 (0x170) / 8
    # UITapGestureRecognizer * _selectGestureRecognizer          196 (0x0C4) / 4       196 (0x0C4) / 4       376 (0x178) / 8       376 (0x178) / 8
    # struct {
    #         unsigned int reversesTitleShadowWhenHighlighted:1;
    #         unsigned int adjustsImageWhenHighlighted:1;
    #         unsigned int adjustsImageWhenDisabled:1;
    #         unsigned int autosizeToFit:1;
    #         unsigned int disabledDimsImage:1;
    #         unsigned int showsTouchWhenHighlighted:1;
    #         unsigned int buttonType:8;
    #         unsigned int shouldHandleScrollerMouseEvent:1;
    #         unsigned int titleFrozen:1;
    #     } _buttonFlags                                         200 (0x0C8) / 2  + 2  200 (0x0C8) / 4       384 (0x180) / 4  + 4  384 (0x180) / 4  + 4
    # _UIButtonMaskAnimationView * _maskAnimationView            204 (0x0CC) / 4       204 (0x0CC) / 4       392 (0x188) / 8       392 (0x188) / 8
    # UIView * _selectionView                                    208 (0x0D0) / 4       208 (0x0D0) / 4       400 (0x190) / 8       400 (0x190) / 8
    # UIFont * _lazyTitleViewFont                                212 (0x0D4) / 4       212 (0x0D4) / 4       408 (0x198) / 8       408 (0x198) / 8
    # NSArray * _contentConstraints                              216 (0x0D8) / 4       216 (0x0D8) / 4       416 (0x1A0) / 8       416 (0x1A0) / 8
    # UIEdgeInsets _internalTitlePaddingInsets                   220 (0x0DC) / 16      220 (0x0DC) / 16      424 (0x1A8) / 32      424 (0x1A8) / 32

    def __init__(self, value_obj, internal_dict):
        super(UIButton_SynthProvider, self).__init__(value_obj, internal_dict)

        self.label = None
        self.label_provider = None

    def get_label(self):
        if self.label:
            return self.label

        self.label = self.get_child_value("_titleView")
        return self.label

    def get_label_provider(self):
        if self.label_provider:
            return self.label_provider

        label = self.get_label()
        self.label_provider = UILabel.UILabel_SynthProvider(label, self.internal_dict)
        return self.label_provider

    def get_label_text(self):
        label_provider = self.get_label_provider()
        label_text = label_provider.get_text()
        return label_text

    def summary(self):
        label_text = self.get_label_text()
        label_text_value = label_text.GetSummary()
        label_summary = "text={}".format(label_text_value)

        return label_summary


def UIButton_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIButton_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIButton.UIButton_SummaryProvider \
                            --category UIKit \
                            UIButton")
    debugger.HandleCommand("type category enable UIKit")
