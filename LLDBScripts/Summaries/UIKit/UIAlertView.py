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
import UILabel
import UIButton


class UIAlertView_SynthProvider(UIView.UIView_SynthProvider):
    # Class: UIAlertView
    # Super class: UIView
    # Name:                                                             armv7                 i386                  arm64                 x86_64
    # id <UIAlertViewDelegate> _delegate                             96 (0x060) / 4        96 (0x060) / 4       184 (0x0B8) / 8       184 (0x0B8) / 8
    # UILabel * _titleLabel                                         100 (0x064) / 4       100 (0x064) / 4       192 (0x0C0) / 8       192 (0x0C0) / 8
    # UILabel * _subtitleLabel                                      104 (0x068) / 4       104 (0x068) / 4       200 (0x0C8) / 8       200 (0x0C8) / 8
    # UILabel * _bodyTextLabel                                      108 (0x06C) / 4       108 (0x06C) / 4       208 (0x0D0) / 8       208 (0x0D0) / 8
    # UILabel * _taglineTextLabel                                   112 (0x070) / 4       112 (0x070) / 4       216 (0x0D8) / 8       216 (0x0D8) / 8
    # CGFloat _startY                                               116 (0x074) / 4       116 (0x074) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # CGPoint _center                                               120 (0x078) / 8       120 (0x078) / 8       232 (0x0E8) / 16      232 (0x0E8) / 16
    # id _context                                                   128 (0x080) / 4       128 (0x080) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # NSInteger _cancelButton                                       132 (0x084) / 4       132 (0x084) / 4       256 (0x100) / 8       256 (0x100) / 8
    # NSInteger _defaultButton                                      136 (0x088) / 4       136 (0x088) / 4       264 (0x108) / 8       264 (0x108) / 8
    # NSInteger _firstOtherButton                                   140 (0x08C) / 4       140 (0x08C) / 4       272 (0x110) / 8       272 (0x110) / 8
    # UIToolbar * _toolbar                                          144 (0x090) / 4       144 (0x090) / 4       280 (0x118) / 8       280 (0x118) / 8
    # UIWindow * _originalWindow                                    148 (0x094) / 4       148 (0x094) / 4       288 (0x120) / 8       288 (0x120) / 8
    # UIWindow * _dimWindow                                         152 (0x098) / 4       152 (0x098) / 4       296 (0x128) / 8       296 (0x128) / 8
    # NSInteger _suspendTag                                         156 (0x09C) / 4       156 (0x09C) / 4       304 (0x130) / 8       304 (0x130) / 8
    # NSInteger _dismissButtonIndex                                 160 (0x0A0) / 4       160 (0x0A0) / 4       312 (0x138) / 8       312 (0x138) / 8
    # CGFloat _bodyTextHeight                                       164 (0x0A4) / 4       164 (0x0A4) / 4       320 (0x140) / 8       320 (0x140) / 8
    # NSMutableArray * _buttons                                     168 (0x0A8) / 4       168 (0x0A8) / 4       328 (0x148) / 8       328 (0x148) / 8
    # NSMutableArray * _textFields                                  172 (0x0AC) / 4       172 (0x0AC) / 4       336 (0x150) / 8       336 (0x150) / 8
    # UIView * _keyboard                                            176 (0x0B0) / 4       176 (0x0B0) / 4       344 (0x158) / 8       344 (0x158) / 8
    # UIView * _table                                               180 (0x0B4) / 4       180 (0x0B4) / 4       352 (0x160) / 8       352 (0x160) / 8
    # UIView * _dimView                                             184 (0x0B8) / 4       184 (0x0B8) / 4       360 (0x168) / 8       360 (0x168) / 8
    # UIView * _backgroundImageView                                 188 (0x0BC) / 4       188 (0x0BC) / 4       368 (0x170) / 8       368 (0x170) / 8
    # UIView * _contentViewNeue                                     192 (0x0C0) / 4       192 (0x0C0) / 4       376 (0x178) / 8       376 (0x178) / 8
    # UIView * _textFieldBackgroundView                             196 (0x0C4) / 4       196 (0x0C4) / 4       384 (0x180) / 8       384 (0x180) / 8
    # UIWindow * _blurWindow                                        200 (0x0C8) / 4       200 (0x0C8) / 4       392 (0x188) / 8       392 (0x188) / 8
    # UIView * _backdropView                                        204 (0x0CC) / 4       204 (0x0CC) / 4       400 (0x190) / 8       400 (0x190) / 8
    # NSMutableDictionary * _separatorsViews                        208 (0x0D0) / 4       208 (0x0D0) / 4       408 (0x198) / 8       408 (0x198) / 8
    # struct {
    #         unsigned int numberOfRows:7;
    #         unsigned int delegateAlertSheetButtonClicked:1;
    #         unsigned int delegateDidPresentAlertSheet:1;
    #         unsigned int delegateDidDismissAlertSheet:1;
    #         unsigned int hideButtonBar:1;
    #         unsigned int alertStyle:3;
    #         unsigned int dontDimBackground:1;
    #         unsigned int dismissSuspended:1;
    #         unsigned int dontBlockInteraction:1;
    #         unsigned int sheetWasPoppedUp:1;
    #         unsigned int animating:1;
    #         unsigned int hideWhenDoneAnimating:1;
    #         unsigned int layoutWhenDoneAnimating:1;
    #         unsigned int titleMaxLineCount:2;
    #         unsigned int bodyTextMaxLineCount:3;
    #         unsigned int runsModal:1;
    #         unsigned int runningModal:1;
    #         unsigned int addedTextView:1;
    #         unsigned int addedTableShadows:1;
    #         unsigned int showOverSBAlerts:1;
    #         unsigned int showMinTableContent:1;
    #         unsigned int bodyTextTruncated:1;
    #         unsigned int orientation:3;
    #         unsigned int groupsTextFields:1;
    #         unsigned int includesCancel:1;
    #         unsigned int useUndoStyle:1;
    #         unsigned int delegateBodyTextAlignment:1;
    #         unsigned int delegateClickedButtonAtIndex:1;
    #         unsigned int delegateClickedButtonAtIndex2:1;
    #         unsigned int delegateCancel:1;
    #         unsigned int delegateCancel2:1;
    #         unsigned int delegateWillPresent:1;
    #         unsigned int delegateWillPresent2:1;
    #         unsigned int delegateDidPresent:1;
    #         unsigned int delegateDidPresent2:1;
    #         unsigned int delegateWillDismiss:1;
    #         unsigned int delegateWillDismiss2:1;
    #         unsigned int delegateDidDismiss:1;
    #         unsigned int delegateDidDismiss2:1;
    #         unsigned int delegateShouldEnableFirstOtherButton:1;
    #         unsigned int forceHorizontalButtonsLayout:1;
    #         unsigned int suppressKeyboardOnPopup:1;
    #         unsigned int keyboardShowing:1;
    #         unsigned int dontCallDismissDelegate:1;
    #         unsigned int useAutomaticKB:1;
    #         unsigned int manualKeyboardVisible:1;
    #         unsigned int rotatingManualKeybaord:1;
    #         unsigned int shouldHandleFirstKeyUpEvent:1;
    #         unsigned int forceKeyboardUse:1;
    #         unsigned int cancelWhenDoneAnimating:1;
    #         unsigned int alertViewStyle:3;
    #         unsigned int isSBAlert:1;
    #         unsigned int isBeingDismissed:1;
    #         unsigned int useLookNeue:1;
    #     } _modalViewFlags                                         212 (0x0D4) / 9  + 3  212 (0x0D4) / 12      416 (0x1A0) / 12 + 4  416 (0x1A0) / 12 + 4
    # NSMutableArray * _buttonTitlesNeue                            224 (0x0E0) / 4       224 (0x0E0) / 4       432 (0x1B0) / 8       432 (0x1B0) / 8
    # NSString * _titleTextNeue                                     228 (0x0E4) / 4       228 (0x0E4) / 4       440 (0x1B8) / 8       440 (0x1B8) / 8
    # NSString * _messageTextNeue                                   232 (0x0E8) / 4       232 (0x0E8) / 4       448 (0x1C0) / 8       448 (0x1C0) / 8
    # UIViewController * _hostingViewControllerNeue                 236 (0x0EC) / 4       236 (0x0EC) / 4       456 (0x1C8) / 8       456 (0x1C8) / 8
    # UIWindow * _windowFOrSBNeueCompatibility                      240 (0x0F0) / 4       240 (0x0F0) / 4       464 (0x1D0) / 8       464 (0x1D0) / 8
    # UIView * _accessoryView                                       244 (0x0F4) / 4       244 (0x0F4) / 4       472 (0x1D8) / 8       472 (0x1D8) / 8
    # UIViewController * _accessoryViewController                   248 (0x0F8) / 4       248 (0x0F8) / 4       480 (0x1E0) / 8       480 (0x1E0) / 8
    # BOOL _textFieldsHidden                                        252 (0x0FC) / 1  + 3  252 (0x0FC) / 1  + 3  488 (0x1E8) / 1  + 7  488 (0x1E8) / 1  + 7
    # _UIModalItem * _representedModalItem                          256 (0x100) / 4       256 (0x100) / 4       496 (0x1F0) / 8       496 (0x1F0) / 8
    # _UIAlertExternalViewController * _externalAlertViewController 260 (0x104) / 4       260 (0x104) / 4       504 (0x1F8) / 8       504 (0x1F8) / 8
    # UIViewController * externalViewControllerForPresentation      264 (0x108) / 4       264 (0x108) / 4       512 (0x200) / 8       512 (0x200) / 8

    def __init__(self, value_obj, internal_dict):
        super(UIAlertView_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIAlertView"

        self.title = None
        self.title_provider = None
        self.subtitle = None
        self.subtitle_provider = None
        self.body = None
        self.body_provider = None
        self.buttons = None

    def get_title(self):
        if self.title:
            return self.title

        self.title = self.get_child_value("_titleLabel")
        return self.title

    def get_title_provider(self):
        if self.title_provider:
            return self.title_provider

        title = self.get_title()
        if title:
            self.title_provider = UILabel.UILabel_SynthProvider(title, self.internal_dict)
        return self.title_provider

    def get_title_value(self):
        title_provider = self.get_title_provider()
        if title_provider is None:
            return None
        return title_provider.get_text_value()

    def get_title_summary(self):
        title_value = self.get_title_value()
        if title_value is None:
            return None
        return "title={}".format(self.get_title_value())

    def get_subtitle(self):
        if self.subtitle:
            return self.subtitle

        self.subtitle = self.get_child_value("_subtitleLabel")
        return self.subtitle

    def get_subtitle_provider(self):
        if self.subtitle_provider:
            return self.subtitle_provider

        subtitle = self.get_subtitle()
        if subtitle:
            self.subtitle_provider = UILabel.UILabel_SynthProvider(subtitle, self.internal_dict)
        return self.subtitle_provider

    def get_subtitle_value(self):
        subtitle_provider = self.get_subtitle_provider()
        if subtitle_provider is None:
            return None
        return subtitle_provider.get_text_value()

    def get_subtitle_summary(self):
        subtitle_text = self.get_subtitle_value()
        if subtitle_text is None:
            return None
        return "subtitle={}".format(self.get_subtitle_value())

    def get_body(self):
        if self.body:
            return self.body

        self.body = self.get_child_value("_bodyTextLabel")
        return self.body

    def get_body_provider(self):
        if self.body_provider:
            return self.body_provider

        body = self.get_body()
        if body:
            self.body_provider = UILabel.UILabel_SynthProvider(body, self.internal_dict)
        return self.body_provider

    def get_body_value(self):
        body_provider = self.get_body_provider()
        if body_provider is None:
            return None
        return body_provider.get_text_value()

    def get_body_summary(self):
        body_value = self.get_body_value()
        if body_value is None:
            return None
        return "message={}".format(body_value)

    def get_buttons(self):
        if self.buttons:
            return self.buttons

        buttons = self.get_child_value("_buttons")
        self.buttons = []
        for i in xrange(0, buttons.GetNumChildren()):
            b = buttons.GetChildAtIndex(i)
            self.buttons.append(b)
        return buttons

    def get_buttons_names(self):
        buttons = self.get_buttons()
        buttons_names = []
        for button in buttons:
            button_provider = UIButton.UIButton_SynthProvider(button, self.internal_dict)
            button_label_text = button_provider.get_label_value()
            if button_label_text:
                buttons_names.append(button_label_text)
        return buttons_names

    def get_buttons_summary(self):
        return "buttons=[{}]".format(", ".join(self.get_buttons_names()))

    def summary(self):
        title_summary = self.get_title_summary()
        subtitle_summary = self.get_subtitle_summary()
        body_summary = self.get_body_summary()
        buttons_names = self.get_buttons_names()
        buttons_summary = self.get_buttons_summary()

        # Summaries
        summaries = []
        if title_summary:
            summaries.append(title_summary)
        if subtitle_summary:
            summaries.append(subtitle_summary)
        if body_summary:
            summaries.append(body_summary)
        if len(buttons_names) > 0:
            summaries.append(buttons_summary)

        summary = ", ".join(summaries)
        return summary


def UIAlertView_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIAlertView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIAlertView.UIAlertView_SummaryProvider \
                            --category UIKit \
                            UIAlertView")
    debugger.HandleCommand("type category enable UIKit")
