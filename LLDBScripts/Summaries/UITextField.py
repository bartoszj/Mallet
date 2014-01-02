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


class UITextField_SynthProvider(UIControl.UIControl_SynthProvider):
    # UITextField:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # _UICascadingTextStorage *_textStorage                                 120 = 0x78 / 4          224 = 0xe0 / 8
    # NSInteger _borderStyle                                                124 = 0x7c / 4          232 = 0xe8 / 8
    # CGFloat _minimumFontSize                                              128 = 0x80 / 4          240 = 0xf0 / 8
    # id _delegate                                                          132 = 0x84 / 4          248 = 0xf8 / 8
    # UIImage *_background                                                  136 = 0x88 / 4          256 = 0x100 / 8
    # UIImage *_disabledBackground                                          140 = 0x8c / 4          264 = 0x108 / 8
    # NSInteger _clearButtonMode                                            144 = 0x90 / 4          272 = 0x110 / 8
    # UIView *_leftView                                                     148 = 0x94 / 4          280 = 0x118 / 8
    # NSInteger _leftViewMode                                               152 = 0x98 / 4          288 = 0x120 / 8
    # UIView *_rightView                                                    156 = 0x9c / 4          296 = 0x128 / 8
    # NSInteger _rightViewMode                                              160 = 0xa0 / 4          304 = 0x130 / 8
    # UITextInputTraits *_traits                                            164 = 0xa4 / 4          312 = 0x138 / 8
    # UITextInputTraits *_nonAtomTraits                                     168 = 0xa8 / 4          320 = 0x140 / 8
    # CGFloat _fullFontSize                                                 172 = 0xac / 4          328 = 0x148 / 8
    # UIEdgeInsets _padding                                                 176 = 0xb0 / 16         336 = 0x150 / 32
    # NSRange _selectionRangeWhenNotEditing                                 192 = 0xc0 / 8          368 = 0x170 / 16
    # int _scrollXOffset                                                    200 = 0xc8 / 4          384 = 0x180 / 4
    # int _scrollYOffset                                                    204 = 0xcc / 4          388 = 0x184 / 4
    # float _progress                                                       208 = 0xd0 / 4          392 = 0x188 / 4 + 4
    # UIButton *_clearButton                                                212 = 0xd4 / 4          400 = 0x190 / 8
    # CGSize _clearButtonOffset                                             216 = 0xd8 / 8          408 = 0x198 / 16
    # CGSize _leftViewOffset                                                224 = 0xe0 / 8          424 = 0x1a8 / 16
    # CGSize _rightViewOffset                                               232 = 0xe8 / 8          440 = 0x1b8 / 16
    # UITextFieldBorderView *_backgroundView                                240 = 0xf0 / 4          456 = 0x1c8 / 8
    # UITextFieldBorderView *_disabledBackgroundView                        244 = 0xf4 / 4          464 = 0x1d0 / 8
    # UITextFieldBackgroundView *_systemBackgroundView                      248 = 0xf8 / 4          472 = 0x1d8 / 8
    # UITextFieldLabel *_displayLabel                                       252 = 0xfc / 4          480 = 0x1e0 / 8
    # UITextFieldLabel *_placeholderLabel                                   256 = 0x100 / 4         488 = 0x1e8 / 8
    # UITextFieldLabel *_suffixLabel                                        260 = 0x104 / 4         496 = 0x1f0 / 8
    # UITextFieldLabel *_prefixLabel                                        264 = 0x108 / 4         504 = 0x1f8 / 8
    # UIImageView *_iconView                                                268 = 0x10c / 4         512 = 0x200 / 8
    # UILabel *_label                                                       272 = 0x110 / 4         520 = 0x208 / 8
    # CGFloat _labelOffset                                                  276 = 0x114 / 4         528 = 0x210 / 8
    # UITextInteractionAssistant *_interactionAssistant                     280 = 0x118 / 4         536 = 0x218 / 8
    # UIView *_inputView                                                    284 = 0x11c / 4         544 = 0x220 / 8
    # UIView *_inputAccessoryView                                           288 = 0x120 / 4         552 = 0x228 / 8
    # UITextFieldAtomBackgroundView *_atomBackgroundView                    292 = 0x124 / 4         560 = 0x230 / 8
    # struct {
    #     unsigned verticallyCenterText : 1
    #     unsigned isAnimating : 4
    #     unsigned inactiveHasDimAppearance : 1
    #     unsigned becomesFirstResponderOnClearButtonTap : 1
    #     unsigned clearsPlaceholderOnBeginEditing : 1
    #     unsigned adjustsFontSizeToFitWidth : 1
    #     unsigned fieldEditorAttached : 1
    #     unsigned canBecomeFirstResponder : 1
    #     unsigned shouldSuppressShouldBeginEditing : 1
    #     unsigned inResignFirstResponder : 1
    #     unsigned undoDisabled : 1
    #     unsigned explicitAlignment : 1
    #     unsigned implementsCustomDrawing : 1
    #     unsigned needsClearing : 1
    #     unsigned suppressContentChangedNotification : 1
    #     unsigned allowsEditingTextAttributes : 1
    #     unsigned usesAttributedText : 1
    #     unsigned backgroundViewState : 2
    #     unsigned clearingBehavior : 2
    # } _textFieldFlags                                                     296 = 0x128 / 3         568 = 0x238 / 3
    # BOOL _deferringBecomeFirstResponder                                   299 = 0x12b / 1         571 = 0x23b / 1
    # BOOL _avoidBecomeFirstResponder                                       300 = 0x12c / 1         572 = 0x23c / 1
    # BOOL _setSelectionRangeAfterFieldEditorIsAttached                     301 = 0x12d / 1         573 = 0x23d / 1
    # BOOL _originFromBaselineLayoutIsInvalid;                              302 = 0x12e / 1 + 1     574 = 0x23e / 1 + 1
    # NSLayoutConstraint *_baselineLayoutConstraint                         304 = 0x130 / 4         576 = 0x240 / 8
    # _UIBaselineLayoutStrut *_baselineLayoutLabel                          308 = 0x134 / 4         584 = 0x248 / 8
    # NSDictionary *_defaultTextAttributes                                  312 = 0x138 / 4         592 = 0x250 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        # self.as_super = super(UITextField_SynthProvider, self)
        # self.as_super.__init__(value_obj, sys_params, internal_dict)
        super(UITextField_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        if not self.sys_params.types_cache.UILabel:
            self.sys_params.types_cache.UILabel = self.value_obj.GetTarget().FindFirstType('UILabel').GetPointerType()

        self.display_label = None
        self.placeholder_label = None

        self.update()

    def update(self):
        self.display_label = None
        self.placeholder_label = None
        super(UITextField_SynthProvider, self).update()

    def adjust_for_architecture(self):
        super(UITextField_SynthProvider, self).adjust_for_architecture()

    def get_display_label(self):
        if self.display_label:
            return self.display_label

        if self.sys_params.is_64_bit:
            offset = 0x1e0
        else:
            offset = 0xfc

        self.display_label = self.value_obj.CreateChildAtOffset("displayasdasLabel",
                                                                offset,
                                                                self.sys_params.types_cache.UILabel)
        return self.display_label

    def get_placeholder_label(self):
        if self.placeholder_label:
            return self.placeholder_label

        if self.sys_params.is_64_bit:
            offset = 0x1e8
        else:
            offset = 0x100

        self.placeholder_label = self.value_obj.CreateChildAtOffset("placeholderLabel",
                                                                    offset,
                                                                    self.sys_params.types_cache.UILabel)
        return self.placeholder_label

    def summary(self):
        # Display label doesn't work :(
        # display_label = self.get_display_label()
        # display_label_provider = UILabel.UILabel_SynthProvider(display_label, self.sys_params, self.internal_dict)
        # display_label_text = display_label_provider.get_text()
        # display_label_text_value = display_label_text.GetSummary()
        # display_label_text_summary = "text={}".format(display_label_text_value)

        placeholder_label = self.get_placeholder_label()
        placeholder_label_provider = UILabel.UILabel_SynthProvider(placeholder_label,
                                                                   self.sys_params,
                                                                   self.internal_dict)
        placeholder_label_text = placeholder_label_provider.get_text()
        placeholder_label_text_value = placeholder_label_text.GetSummary()
        placeholder_label_text_summary = "placeholder={}".format(placeholder_label_text_value)

        # Summary
        summaries = []
        # if display_label_text_value:
        #     summaries.append(display_label_text_summary)
        if placeholder_label_text_value:
            summaries.append(placeholder_label_text_summary)

        summary = ", ".join(summaries)
        return summary


def UITextField_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UITextField_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UITextField.UITextField_SummaryProvider \
                            --category UIKit \
                            UITextField")
    debugger.HandleCommand("type category enable UIKit")
