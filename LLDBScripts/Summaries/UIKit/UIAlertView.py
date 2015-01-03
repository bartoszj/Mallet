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

    @Helpers.save_parameter("title")
    def get_title(self):
        return self.get_child_value("_titleLabel")

    @Helpers.save_parameter("title_provider")
    def get_title_provider(self):
        title = self.get_title()
        return None if title is None else UILabel.UILabel_SynthProvider(title, self.internal_dict)

    def get_title_value(self):
        title_provider = self.get_title_provider()
        return None if title_provider is None else title_provider.get_text_value()

    def get_title_summary(self):
        title_value = self.get_title_value()
        return None if title_value is None else "title={}".format(self.get_title_value())

    @Helpers.save_parameter("subtitle")
    def get_subtitle(self):
        return self.get_child_value("_subtitleLabel")

    @Helpers.save_parameter("subtitle_provider")
    def get_subtitle_provider(self):
        subtitle = self.get_subtitle()
        return None if subtitle is None else UILabel.UILabel_SynthProvider(subtitle, self.internal_dict)

    def get_subtitle_value(self):
        subtitle_provider = self.get_subtitle_provider()
        return None if subtitle_provider is None else subtitle_provider.get_text_value()

    def get_subtitle_summary(self):
        subtitle_text = self.get_subtitle_value()
        return None if subtitle_text is None else "subtitle={}".format(self.get_subtitle_value())

    @Helpers.save_parameter("body")
    def get_body(self):
        return self.get_child_value("_bodyTextLabel")

    @Helpers.save_parameter("body_provider")
    def get_body_provider(self):
        body = self.get_body()
        return None if body is None else UILabel.UILabel_SynthProvider(body, self.internal_dict)

    def get_body_value(self):
        body_provider = self.get_body_provider()
        return None if body_provider is None else body_provider.get_text_value()

    def get_body_summary(self):
        body_value = self.get_body_value()
        return None if body_value is None else "message={}".format(body_value)

    @Helpers.save_parameter("buttons")
    def get_buttons(self):
        return self.get_child_value("_buttons")

    def get_buttons_objects(self):
        buttons = self.get_buttons()
        if buttons is None:
            return None

        buttons_objects = []
        for i in xrange(0, get_count_value(buttons)):
            b = buttons.GetChildAtIndex(i)
            buttons_objects.append(b)
        return buttons_objects

    def get_buttons_names(self):
        buttons = self.get_buttons_objects()
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
