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
import UIView
import UILabel
import UIButton


class UIAlertView_SynthProvider(UIView.UIView_SynthProvider):
    # UILabel:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # id<UIAlertViewDelegate> _delegate                                      96 = 0x60 / 4          184 = 0xb8 / 8
    # UILabel *_titleLabel                                                  100 = 0x64 / 4          192 = 0xc0 / 8
    # UILabel *_subtitleLabel                                               104 = 0x68 / 4          200 = 0xc8 / 8
    # UILabel *_bodyTextLabel                                               108 = 0x6c / 4          208 = 0xd0 / 8
    # UILabel *_taglineTextLabel                                            112 = 0x70 / 4          216 = 0xd8 / 8
    # CGFloat _startY                                                       116 = 0x74 / 4          224 = 0xe0 / 8
    # CGPoint _center                                                       120 = 0x78 / 8          232 = 0xe8 / 16
    # id _context                                                           128 = 0x80 / 4          248 = 0xf8 / 8
    # NSInteger _cancelButton                                               132 = 0x84 / 4          256 = 0x100 / 8
    # NSInteger _defaultButton                                              136 = 0x88 / 4          264 = 0x108 / 8
    # NSInteger _firstOtherButton                                           140 = 0x8c / 4          272 = 0x110 / 8
    # UIToolbar *_toolbar                                                   144 = 0x90 / 4          280 = 0x118 / 8
    # UIWindow *_originalWindow                                             148 = 0x94 / 4          288 = 0x120 / 8
    # UIWindow *_dimWindow                                                  152 = 0x98 / 4          296 = 0x128 / 8
    # NSInteger _suspendTag                                                 156 = 0x9c / 4          304 = 0x130 / 8
    # NSInteger _dismissButtonIndex                                         160 = 0xa0 / 4          312 = 0x138 / 8
    # CGFloat _bodyTextHeight                                               164 = 0xa4 / 4          320 = 0x140 / 8
    # NSMutableArray *_buttons                                              168 = 0xa8 / 4          328 = 0x148 / 8
    # NSMutableArray *_textFields                                           172 = 0xac / 4          336 = 0x150 / 8
    # UIView *_keyboard                                                     176 = 0xb0 / 4          344 = 0x158 / 8
    # UIView *_table                                                        180 = 0xb4 / 4          352 = 0x160 / 8
    # UIView *_dimView                                                      184 = 0xb8 / 4          360 = 0x168 / 8
    # UIView *_backgroundImageView                                          188 = 0xbc / 4          368 = 0x170 / 8
    # UIView *_contentViewNeue                                              192 = 0xc0 / 4          376 = 0x178 / 8
    # UIView *_textFieldBackgroundView                                      196 = 0xc4 / 4          384 = 0x180 / 8
    # UIWindow *_blurWindow                                                 200 = 0xc8 / 4          392 = 0x188 / 8
    # UIView *_backdropView                                                 204 = 0xcc / 4          400 = 0x190 / 8
    # NSMutableDictionary *_separatorsViews                                 208 = 0xd0 / 4          408 = 0x198 / 8
    # struct {
    #     unsigned numberOfRows : 7
    #     unsigned delegateAlertSheetButtonClicked : 1
    #     unsigned delegateDidPresentAlertSheet : 1
    #     unsigned delegateDidDismissAlertSheet : 1
    #     unsigned hideButtonBar : 1
    #     unsigned alertStyle : 3
    #     unsigned dontDimBackground : 1
    #     unsigned dismissSuspended : 1
    #     unsigned dontBlockInteraction : 1
    #     unsigned sheetWasPoppedUp : 1
    #     unsigned animating : 1
    #     unsigned hideWhenDoneAnimating : 1
    #     unsigned layoutWhenDoneAnimating : 1
    #     unsigned titleMaxLineCount : 2
    #     unsigned bodyTextMaxLineCount : 3
    #     unsigned runsModal : 1
    #     unsigned runningModal : 1
    #     unsigned addedTextView : 1
    #     unsigned addedTableShadows : 1
    #     unsigned showOverSBAlerts : 1
    #     unsigned showMinTableContent : 1
    #     unsigned bodyTextTruncated : 1
    #     unsigned orientation : 3
    #     unsigned groupsTextFields : 1
    #     unsigned includesCancel : 1
    #     unsigned useUndoStyle : 1
    #     unsigned delegateBodyTextAlignment : 1
    #     unsigned delegateClickedButtonAtIndex : 1
    #     unsigned delegateClickedButtonAtIndex2 : 1
    #     unsigned delegateCancel : 1
    #     unsigned delegateCancel2 : 1
    #     unsigned delegateWillPresent : 1
    #     unsigned delegateWillPresent2 : 1
    #     unsigned delegateDidPresent : 1
    #     unsigned delegateDidPresent2 : 1
    #     unsigned delegateWillDismiss : 1
    #     unsigned delegateWillDismiss2 : 1
    #     unsigned delegateDidDismiss : 1
    #     unsigned delegateDidDismiss2 : 1
    #     unsigned delegateShouldEnableFirstOtherButton : 1
    #     unsigned forceHorizontalButtonsLayout : 1
    #     unsigned suppressKeyboardOnPopup : 1
    #     unsigned keyboardShowing : 1
    #     unsigned dontCallDismissDelegate : 1
    #     unsigned useAutomaticKB : 1
    #     unsigned manualKeyboardVisible : 1
    #     unsigned rotatingManualKeybaord : 1
    #     unsigned shouldHandleFirstKeyUpEvent : 1
    #     unsigned forceKeyboardUse : 1
    #     unsigned cancelWhenDoneAnimating : 1
    #     unsigned alertViewStyle : 3
    #     unsigned isSBAlert : 1
    #     unsigned isBeingDismissed : 1
    #     unsigned useLookNeue : 1
    # } _modalViewFlags                                                     212 = 0xd4 / 9 + 3      416 = 0x1a0 / 9 + 7
    # NSMutableArray *_buttonTitlesNeue                                     224 = 0xe0 / 4          432 = 0x1b0 / 8
    # NSString *_titleTextNeue                                              228 = 0xe4 / 4          440 = 0x1b8 / 8
    # NSString *_messageTextNeue                                            232 = 0xe8 / 4          448 = 0x1c0 / 8
    # UIViewController *_hostingViewControllerNeue                          236 = 0xec / 4          456 = 0x1c8 / 8
    # UIWindow *_windowFOrSBNeueCompatibility                               240 = 0xf0 / 4          464 = 0x1d0 / 8
    # UIView *_accessoryView                                                244 = 0xf4 / 4          472 = 0x1d8 / 8
    # UIViewController *_accessoryViewController                            248 = 0xf8 / 4          480 = 0x1e0 / 8
    # BOOL _textFieldsHidden                                                252 = 0xfc / 1 + 3      488 = 0x1e8 / 1 + 7
    # _UIModalItem *_representedModalItem                                   256 = 0x100 / 4         496 = 0x1f0 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UIAlertView_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        if not self.sys_params.types_cache.UILabel:
            self.sys_params.types_cache.UILabel = self.value_obj.GetTarget().FindFirstType('UILabel').GetPointerType()

        self.title = None
        self.subtitle = None
        self.body = None
        self.buttons = None

        self.update()

    def update(self):
        self.title = None
        self.subtitle = None
        self.body = None
        self.buttons = None
        super(UIAlertView_SynthProvider, self).update()

    def get_title(self):
        if self.title:
            return self.title

        if self.sys_params.is_64_bit:
            offset = 0xc0
        else:
            offset = 0x64

        self.title = self.value_obj.CreateChildAtOffset("titleLabel",
                                                        offset,
                                                        self.sys_params.types_cache.UILabel)
        return self.title

    def get_subtitle(self):
        if self.subtitle:
            return self.subtitle

        if self.sys_params.is_64_bit:
            offset = 0xc8
        else:
            offset = 0x68

        self.subtitle = self.value_obj.CreateChildAtOffset("subtitleLabel",
                                                           offset,
                                                           self.sys_params.types_cache.UILabel)
        return self.subtitle

    def get_body(self):
        if self.body:
            return self.body

        if self.sys_params.is_64_bit:
            offset = 0xd0
        else:
            offset = 0x6c

        self.body = self.value_obj.CreateChildAtOffset("bodyLabel",
                                                       offset,
                                                       self.sys_params.types_cache.UILabel)
        return self.body

    def get_buttons(self):
        if self.buttons:
            return self.buttons

        if self.sys_params.is_64_bit:
            offset = 0x138
        else:
            offset = 0xa8

        buttons = self.value_obj.CreateChildAtOffset("buttons",
                                                     offset,
                                                     self.sys_params.types_cache.NSArray)
        self.buttons = []
        for i in xrange(0, buttons.GetNumChildren()):
            b = buttons.GetChildAtIndex(i)
            self.buttons.append(b)
        return buttons

    def summary(self):
        title = self.get_title()
        title_provider = UILabel.UILabel_SynthProvider(title, self.sys_params, self.internal_dict)
        title_text = title_provider.get_text()
        title_text_value = title_text.GetSummary()
        title_summary = "title={}".format(title_text_value)

        subtitle = self.get_subtitle()
        subtitle_provider = UILabel.UILabel_SynthProvider(subtitle, self.sys_params, self.internal_dict)
        subtitle_text = subtitle_provider.get_text()
        subtitle_text_value = subtitle_text.GetSummary()
        subtitle_summary = "subtitle={}".format(subtitle_text_value)

        body = self.get_body()
        body_provider = UILabel.UILabel_SynthProvider(body, self.sys_params, self.internal_dict)
        body_text = body_provider.get_text()
        body_text_value = body_text.GetSummary()
        body_summary = "message={}".format(body_text_value)

        buttons = self.get_buttons()
        buttons_names = []
        for button in buttons:
            button_provider = UIButton.UIButton_SynthProvider(button, self.sys_params, self.internal_dict)
            button_label_text = button_provider.get_label_text()
            button_label_text_value = button_label_text.GetSummary()
            if button_label_text_value:
                buttons_names.append(button_label_text_value)
        buttons_summary = "buttons=[{}]".format(", ".join(buttons_names))

        # Summaries
        summaries = []
        if title_text_value:
            summaries.append(title_summary)
        if subtitle_text_value:
            summaries.append(subtitle_summary)
        if body_text_value:
            summaries.append(body_summary)
        if len(buttons_names) > 0:
            summaries.append(buttons_summary)
        summary = ", ".join(summaries)
        return summary


def UIAlertView_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIAlertView_SynthProvider)

    # Class data
    # global statistics
    # class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    # if not class_data.is_valid():
    #     return ""
    # summary_helpers.update_sys_params(value_obj, class_data.sys_params)
    # if wrapper is not None:
    #     return wrapper.message()
    #
    # wrapper = UIAlertView_SynthProvider(value_obj, class_data.sys_params, internal_dict)
    # if wrapper is not None:
    #     return wrapper.summary()
    # return "Summary Unavailable"


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIAlertView.UIAlertView_SummaryProvider \
                            --category UIKit \
                            UIAlertView")
    debugger.HandleCommand("type category enable UIKit")
