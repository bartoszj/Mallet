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
import UIControl
import UILabel


class UIButton_SynthProvider(UIControl.UIControl_SynthProvider):
    # UIButton:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # CFDictionaryRef _contentLookup                                        120 = 0x78 / 4          224 = 0xe0 / 8
    # UIEdgeInsets _contentEdgeInsets                                       124 = 0x7c / 16         232 = 0xe8 / 32
    # UIEdgeInsets _titleEdgeInsets                                         140 = 0x8c / 16         264 = 0x108 / 32
    # UIEdgeInsets _imageEdgeInsets                                         156 = 0x9c / 16         296 = 0x128 / 32
    # UIImageView *_backgroundView                                          172 = 0xac / 4          328 = 0x148 / 8
    # UIImageView *_imageView                                               176 = 0xb0 / 4          336 = 0x150 / 8
    # UILabel *_titleView                                                   180 = 0xb4 / 4          344 = 0x158 / 8
    # BOOL _initialized                                                     184 = 0xb8 / 1 + 3      352 = 0x160 / 1 + 7
    # NSUInteger _lastDrawingControlState                                   188 = 0xbc / 4          360 = 0x168 / 8
    # struct {
    #     unsigned reversesTitleShadowWhenHighlighted : 1;
    #     unsigned adjustsImageWhenHighlighted : 1;
    #     unsigned adjustsImageWhenDisabled : 1;
    #     unsigned autosizeToFit : 1;
    #     unsigned disabledDimsImage : 1;
    #     unsigned showsTouchWhenHighlighted : 1;
    #     unsigned buttonType : 8;
    #     unsigned shouldHandleScrollerMouseEvent : 1;
    #     unsigned titleFrozen : 1;
    # } _buttonFlags                                                        192 = 0xc0 / 3 + 1      368 = 0x170 / 3 + 5
    # _UIButtonMaskAnimationView *_maskAnimationView                        196 = 0xc4 / 4          376 = 0x178 / 8
    # UIView *_selectionView                                                200 = 0xcc / 4          384 = 0x180 / 8
    # UIFont *_lazyTitleViewFont                                            204 = 0xd0 / 4          392 = 0x188 / 8
    # NSArray *_contentConstraints                                          208 = 0xd4 / 4          400 = 0x190 / 8
    # UIEdgeInsets _internalTitlePaddingInsets                              212 = 0xd8 / 16         408 = 0x198 / 32

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UIButton_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        if not self.sys_params.types_cache.UILabel:
            self.sys_params.types_cache.UILabel = self.value_obj.GetTarget().FindFirstType('UILabel').GetPointerType()

        self.label = None

        self.update()

    def update(self):
        self.label = None
        super(UIButton_SynthProvider, self).update()

    def get_label(self):
        if self.label:
            return self.label

        if self.sys_params.is_64_bit:
            offset = 0x158
        else:
            offset = 0xb4

        self.label = self.value_obj.CreateChildAtOffset("titleView",
                                                        offset,
                                                        self.sys_params.types_cache.UILabel)
        return self.label

    def get_label_text(self):
        label = self.get_label()
        label_provider = UILabel.UILabel_SynthProvider(label, self.sys_params, self.internal_dict)
        label_text = label_provider.get_text()
        return label_text

    def summary(self):
        label_text = self.get_label_text()
        label_text_value = label_text.GetSummary()
        label_summary = "text={}".format(label_text_value)

        return label_summary


def UIButton_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIButton_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIButton.UIButton_SummaryProvider \
                            --category UIKit \
                            UIButton")
    debugger.HandleCommand("type category enable UIKit")
