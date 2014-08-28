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


class UIPickerView_SynthProvider(UIView.UIView_SynthProvider):
    # Class: UIPickerView
    # Super class: UIView
    # Protocols: UIPickerTableViewContainerDelegate, UITableViewDelegate, UIPickerViewScrollTesting, NSCoding, UITableViewDataSource
    # Name:                                                                        armv7                 i386                  arm64                 x86_64
    # NSMutableArray * _tables                                                  96 (0x060) / 4        96 (0x060) / 4       184 (0x0B8) / 8       184 (0x0B8) / 8
    # UIView * _topFrame                                                       100 (0x064) / 4       100 (0x064) / 4       192 (0x0C0) / 8       192 (0x0C0) / 8
    # NSMutableArray * _dividers                                               104 (0x068) / 4       104 (0x068) / 4       200 (0x0C8) / 8       200 (0x0C8) / 8
    # NSMutableArray * _selectionBars                                          108 (0x06C) / 4       108 (0x06C) / 4       208 (0x0D0) / 8       208 (0x0D0) / 8
    # id <UIPickerViewDataSource> _dataSource                                  112 (0x070) / 4       112 (0x070) / 4       216 (0x0D8) / 8       216 (0x0D8) / 8
    # id <UIPickerViewDelegate> _delegate                                      116 (0x074) / 4       116 (0x074) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # UIView * _backgroundView                                                 120 (0x078) / 4       120 (0x078) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # NSInteger _numberOfComponents                                            124 (0x07C) / 4       124 (0x07C) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # UIImageView * _topGradient                                               128 (0x080) / 4       128 (0x080) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # UIImageView * _bottomGradient                                            132 (0x084) / 4       132 (0x084) / 4       256 (0x100) / 8       256 (0x100) / 8
    # UIView * _foregroundView                                                 136 (0x088) / 4       136 (0x088) / 4       264 (0x108) / 8       264 (0x108) / 8
    # CALayer * _maskGradientLayer                                             140 (0x08C) / 4       140 (0x08C) / 4       272 (0x110) / 8       272 (0x110) / 8
    # UIView * _topLineView                                                    144 (0x090) / 4       144 (0x090) / 4       280 (0x118) / 8       280 (0x118) / 8
    # UIView * _bottomLineView                                                 148 (0x094) / 4       148 (0x094) / 4       288 (0x120) / 8       288 (0x120) / 8
    # struct {
    #         unsigned int needsLayout:1;
    #         unsigned int delegateRespondsToNumberOfComponentsInPickerView:1;
    #         unsigned int delegateRespondsToNumberOfRowsInComponent:1;
    #         unsigned int delegateRespondsToDidSelectRow:1;
    #         unsigned int delegateRespondsToViewForRow:1;
    #         unsigned int delegateRespondsToTitleForRow:1;
    #         unsigned int delegateRespondsToAttributedTitleForRow:1;
    #         unsigned int delegateRespondsToWidthForComponent:1;
    #         unsigned int delegateRespondsToRowHeightForComponent:1;
    #         unsigned int showsSelectionBar:1;
    #         unsigned int allowsMultipleSelection:1;
    #         unsigned int allowSelectingCells:1;
    #         unsigned int soundsDisabled:1;
    #         unsigned int usesCheckedSelection:1;
    #         unsigned int skipsBackground:1;
    #     } _pickerViewFlags                                                   152 (0x098) / 2       152 (0x098) / 4       296 (0x128) / 4       296 (0x128) / 4
    # BOOL _usesModernStyle                                                    154 (0x09A) / 1  + 1  156 (0x09C) / 1  + 3  300 (0x12C) / 1  + 3  300 (0x12C) / 1  + 3
    # UIColor * _textColor                                                     156 (0x09C) / 4       160 (0x0A0) / 4       304 (0x130) / 8       304 (0x130) / 8
    # UIColor * _textShadowColor                                               160 (0x0A0) / 4       164 (0x0A4) / 4       312 (0x138) / 8       312 (0x138) / 8
    # _UIPickerViewTestParameters * _currentTestParameters                     164 (0x0A4) / 4       168 (0x0A8) / 4       320 (0x140) / 8       320 (0x140) / 8
    # BOOL _isInLayoutSubviews                                                 168 (0x0A8) / 1       172 (0x0AC) / 1       328 (0x148) / 1       328 (0x148) / 1
    # BOOL _magnifierEnabled                                                   169 (0x0A9) / 1       173 (0x0AD) / 1       329 (0x149) / 1       329 (0x149) / 1

    def __init__(self, value_obj, internal_dict):
        super(UIPickerView_SynthProvider, self).__init__(value_obj, internal_dict)


def UIPickerView_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIPickerView_SynthProvider)


# def __lldb_init_module(debugger, dict):
#     debugger.HandleCommand("type summary add -F UIPickerView.UIPickerView_SummaryProvider \
#                             --category UIKit \
#                             UIPickerView")
#     debugger.HandleCommand("type category enable UIKit")
