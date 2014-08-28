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


class UITextField_SynthProvider(UIControl.UIControl_SynthProvider):
    # Class: UITextField
    # Super class: UIControl
    # Protocols: UIKeyboardInput, UITextInputTraits_Private, UIPopoverControllerDelegate, UITextInput, NSCoding
    # Name:                                                             armv7                 i386                  arm64                 x86_64
    # _UICascadingTextStorage * _textStorage                        120 (0x078) / 4       120 (0x078) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # NSInteger _borderStyle                                        124 (0x07C) / 4       124 (0x07C) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # CGFloat _minimumFontSize                                      128 (0x080) / 4       128 (0x080) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # id _delegate                                                  132 (0x084) / 4       132 (0x084) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # UIImage * _background                                         136 (0x088) / 4       136 (0x088) / 4       256 (0x100) / 8       256 (0x100) / 8
    # UIImage * _disabledBackground                                 140 (0x08C) / 4       140 (0x08C) / 4       264 (0x108) / 8       264 (0x108) / 8
    # NSInteger _clearButtonMode                                    144 (0x090) / 4       144 (0x090) / 4       272 (0x110) / 8       272 (0x110) / 8
    # UIView * _leftView                                            148 (0x094) / 4       148 (0x094) / 4       280 (0x118) / 8       280 (0x118) / 8
    # NSInteger _leftViewMode                                       152 (0x098) / 4       152 (0x098) / 4       288 (0x120) / 8       288 (0x120) / 8
    # UIView * _rightView                                           156 (0x09C) / 4       156 (0x09C) / 4       296 (0x128) / 8       296 (0x128) / 8
    # NSInteger _rightViewMode                                      160 (0x0A0) / 4       160 (0x0A0) / 4       304 (0x130) / 8       304 (0x130) / 8
    # UITextInputTraits * _traits                                   164 (0x0A4) / 4       164 (0x0A4) / 4       312 (0x138) / 8       312 (0x138) / 8
    # UITextInputTraits * _nonAtomTraits                            168 (0x0A8) / 4       168 (0x0A8) / 4       320 (0x140) / 8       320 (0x140) / 8
    # CGFloat _fullFontSize                                         172 (0x0AC) / 4       172 (0x0AC) / 4       328 (0x148) / 8       328 (0x148) / 8
    # UIEdgeInsets _padding                                         176 (0x0B0) / 16      176 (0x0B0) / 16      336 (0x150) / 32      336 (0x150) / 32
    # struct _NSRange _selectionRangeWhenNotEditing                 192 (0x0C0) / 8       192 (0x0C0) / 8       368 (0x170) / 16      368 (0x170) / 16
    # int _scrollXOffset                                            200 (0x0C8) / 4       200 (0x0C8) / 4       384 (0x180) / 4       384 (0x180) / 4
    # int _scrollYOffset                                            204 (0x0CC) / 4       204 (0x0CC) / 4       388 (0x184) / 4       388 (0x184) / 4
    # float _progress                                               208 (0x0D0) / 4       208 (0x0D0) / 4       392 (0x188) / 4  + 4  392 (0x188) / 4  + 4
    # UIButton * _clearButton                                       212 (0x0D4) / 4       212 (0x0D4) / 4       400 (0x190) / 8       400 (0x190) / 8
    # CGSize _clearButtonOffset                                     216 (0x0D8) / 8       216 (0x0D8) / 8       408 (0x198) / 16      408 (0x198) / 16
    # CGSize _leftViewOffset                                        224 (0x0E0) / 8       224 (0x0E0) / 8       424 (0x1A8) / 16      424 (0x1A8) / 16
    # CGSize _rightViewOffset                                       232 (0x0E8) / 8       232 (0x0E8) / 8       440 (0x1B8) / 16      440 (0x1B8) / 16
    # UITextFieldBorderView * _backgroundView                       240 (0x0F0) / 4       240 (0x0F0) / 4       456 (0x1C8) / 8       456 (0x1C8) / 8
    # UITextFieldBorderView * _disabledBackgroundView               244 (0x0F4) / 4       244 (0x0F4) / 4       464 (0x1D0) / 8       464 (0x1D0) / 8
    # UITextFieldBackgroundView * _systemBackgroundView             248 (0x0F8) / 4       248 (0x0F8) / 4       472 (0x1D8) / 8       472 (0x1D8) / 8
    # UITextFieldLabel * _displayLabel                              252 (0x0FC) / 4       252 (0x0FC) / 4       480 (0x1E0) / 8       480 (0x1E0) / 8
    # UITextFieldLabel * _placeholderLabel                          256 (0x100) / 4       256 (0x100) / 4       488 (0x1E8) / 8       488 (0x1E8) / 8
    # UITextFieldLabel * _suffixLabel                               260 (0x104) / 4       260 (0x104) / 4       496 (0x1F0) / 8       496 (0x1F0) / 8
    # UITextFieldLabel * _prefixLabel                               264 (0x108) / 4       264 (0x108) / 4       504 (0x1F8) / 8       504 (0x1F8) / 8
    # UIImageView * _iconView                                       268 (0x10C) / 4       268 (0x10C) / 4       512 (0x200) / 8       512 (0x200) / 8
    # UILabel * _label                                              272 (0x110) / 4       272 (0x110) / 4       520 (0x208) / 8       520 (0x208) / 8
    # CGFloat _labelOffset                                          276 (0x114) / 4       276 (0x114) / 4       528 (0x210) / 8       528 (0x210) / 8
    # UITextInteractionAssistant * _interactionAssistant            280 (0x118) / 4       280 (0x118) / 4       536 (0x218) / 8       536 (0x218) / 8
    # UIView * _inputView                                           284 (0x11C) / 4       284 (0x11C) / 4       544 (0x220) / 8       544 (0x220) / 8
    # UIView * _inputAccessoryView                                  288 (0x120) / 4       288 (0x120) / 4       552 (0x228) / 8       552 (0x228) / 8
    # UITextFieldAtomBackgroundView * _atomBackgroundView           292 (0x124) / 4       292 (0x124) / 4       560 (0x230) / 8       560 (0x230) / 8
    # struct {
    #         unsigned int verticallyCenterText:1;
    #         unsigned int isAnimating:4;
    #         unsigned int inactiveHasDimAppearance:1;
    #         unsigned int becomesFirstResponderOnClearButtonTap:1;
    #         unsigned int clearsPlaceholderOnBeginEditing:1;
    #         unsigned int adjustsFontSizeToFitWidth:1;
    #         unsigned int fieldEditorAttached:1;
    #         unsigned int canBecomeFirstResponder:1;
    #         unsigned int shouldSuppressShouldBeginEditing:1;
    #         unsigned int inResignFirstResponder:1;
    #         unsigned int undoDisabled:1;
    #         unsigned int explicitAlignment:1;
    #         unsigned int implementsCustomDrawing:1;
    #         unsigned int needsClearing:1;
    #         unsigned int suppressContentChangedNotification:1;
    #         unsigned int allowsEditingTextAttributes:1;
    #         unsigned int usesAttributedText:1;
    #         unsigned int backgroundViewState:2;
    #         unsigned int clearingBehavior:2;
    #     } _textFieldFlags                                         296 (0x128) / 3       296 (0x128) / 4       568 (0x238) / 4       568 (0x238) / 4
    # BOOL _deferringBecomeFirstResponder                           299 (0x12B) / 1       300 (0x12C) / 1       572 (0x23C) / 1       572 (0x23C) / 1
    # BOOL _avoidBecomeFirstResponder                               300 (0x12C) / 1       301 (0x12D) / 1       573 (0x23D) / 1       573 (0x23D) / 1
    # BOOL _setSelectionRangeAfterFieldEditorIsAttached             301 (0x12D) / 1       302 (0x12E) / 1       574 (0x23E) / 1       574 (0x23E) / 1
    # BOOL _originFromBaselineLayoutIsInvalid                       302 (0x12E) / 1  + 1  303 (0x12F) / 1       575 (0x23F) / 1       575 (0x23F) / 1
    # NSLayoutConstraint * _baselineLayoutConstraint                304 (0x130) / 4       304 (0x130) / 4       576 (0x240) / 8       576 (0x240) / 8
    # _UIBaselineLayoutStrut * _baselineLayoutLabel                 308 (0x134) / 4       308 (0x134) / 4       584 (0x248) / 8       584 (0x248) / 8

    def __init__(self, value_obj, internal_dict):
        super(UITextField_SynthProvider, self).__init__(value_obj, internal_dict)

        self.display_label = None
        self.display_label_provider = None
        self.placeholder_label = None
        self.placeholder_label_provider = None

    def get_display_label(self):
        if self.display_label:
            return self.display_label

        self.display_label = self.get_child_value("_displayLabel")
        return self.display_label

    def get_display_label_provider(self):
        if self.display_label_provider:
            return self.display_label_provider

        display_label = self.get_display_label()
        self.display_label_provider = UILabel.UILabel_SynthProvider(display_label, self.internal_dict)
        return self.display_label_provider

    def get_placeholder_label(self):
        if self.placeholder_label:
            return self.placeholder_label

        self.placeholder_label = self.get_child_value("_placeholderLabel")
        return self.placeholder_label

    def get_placeholder_label_provider(self):
        if self.placeholder_label_provider:
            return self.placeholder_label_provider

        placeholder_label = self.get_placeholder_label()
        self.placeholder_label_provider = UILabel.UILabel_SynthProvider(placeholder_label, self.internal_dict)
        return self.placeholder_label_provider

    def summary(self):
        # Display label doesn't work :(
        # display_label_provider = self.get_display_label_provider()
        # display_label_text = display_label_provider.get_text()
        # display_label_text_value = display_label_text.GetSummary()
        # display_label_text_summary = "text={}".format(display_label_text_value)

        placeholder_label_provider = self.get_placeholder_label_provider()
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
    return Helpers.generic_summary_provider(value_obj, internal_dict, UITextField_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UITextField.UITextField_SummaryProvider \
                            --category UIKit \
                            UITextField")
    debugger.HandleCommand("type category enable UIKit")
