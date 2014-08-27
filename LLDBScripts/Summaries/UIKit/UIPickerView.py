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

import summary_helpers
import UIView


class UIPickerView_SynthProvider(UIView.UIView_SynthProvider):
    # UIPickerView:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSMutableArray *_tables                                                96 = 0x60 / 4          184 = 0xb8 / 8
    # UIView *_topFrame                                                     100 = 0x64 / 4          192 = 0xc0 / 8
    # NSMutableArray *_dividers                                             104 = 0x68 / 4          200 = 0xc8 / 8
    # NSMutableArray *_selectionBars                                        108 = 0x6c / 4          208 = 0xd0 / 8
    # id <UIPickerViewDataSource> _dataSource                               112 = 0x70 / 4          216 = 0xd8 / 8
    # id <UIPickerViewDelegate> _delegate                                   116 = 0x74 / 4          224 = 0xe0 / 8
    # UIView *_backgroundView                                               120 = 0x78 / 4          232 = 0xe8 / 8
    # NSInteger _numberOfComponents                                         124 = 0x7c / 4          240 = 0xf0 / 8
    # UIImageView *_topGradient                                             128 = 0x80 / 4          248 = 0xf8 / 8
    # UIImageView *_bottomGradient                                          132 = 0x84 / 4          256 = 0x100 / 8
    # UIView *_foregroundView                                               136 = 0x88 / 4          264 = 0x108 / 8
    # CALayer *_maskGradientLayer                                           140 = 0x8c / 4          272 = 0x110 / 8
    # UIView *_topLineView                                                  144 = 0x90 / 4          280 = 0x118 / 8
    # UIView *_bottomLineView                                               148 = 0x94 / 4          288 = 0x120 / 8
    # struct {
    #     unsigned int needsLayout:1
    #     unsigned int delegateRespondsToNumberOfComponentsInPickerView:1
    #     unsigned int delegateRespondsToNumberOfRowsInComponent:1
    #     unsigned int delegateRespondsToDidSelectRow:1
    #     unsigned int delegateRespondsToViewForRow:1
    #     unsigned int delegateRespondsToTitleForRow:1
    #     unsigned int delegateRespondsToAttributedTitleForRow:1
    #     unsigned int delegateRespondsToWidthForComponent:1
    #     unsigned int delegateRespondsToRowHeightForComponent:1
    #     unsigned int showsSelectionBar:1
    #     unsigned int allowsMultipleSelection:1
    #     unsigned int allowSelectingCells:1
    #     unsigned int soundsDisabled:1
    #     unsigned int usesCheckedSelection:1
    #     unsigned int skipsBackground:1
    # } _pickerViewFlags                                                    152 = 0x98 / 2 + 2      296 = 0x128 / 2 + 2
    # BOOL _usesModernStyle                                                 156 = 0x9c / 1 + 3      300 = 0x12c / 1 + 3
    # UIColor *_textColor                                                   160 = 0xa0 / 4          304 = 0x130 / 8
    # UIColor *_textShadowColor                                             164 = 0xa4 / 4          312 = 0x138 / 8
    # BOOL _isInLayoutSubviews                                              168 = 0xa8 / 1          320 = 0x140 / 1
    # BOOL _magnifierEnabled                                                169 = 0xa9 / 1          321 = 0x141 / 1

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UIPickerView_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)


def UIPickerView_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIPickerView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIPickerView.UIPickerView_SummaryProvider \
                            --category UIKit \
                            UIPickerView")
    debugger.HandleCommand("type category enable UIKit")
