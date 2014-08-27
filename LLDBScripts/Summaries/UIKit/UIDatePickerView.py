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
import UIPickerView


class UIDatePickerView_SynthProvider(UIPickerView.UIPickerView_SynthProvider):
    # _UIDatePickerView:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSInteger _loadingDate                                                172 = 0xac / 4          328 = 0x148 / 8
    # NSDate *_userSuppliedDate                                             176 = 0xb0 / 4          336 = 0x150 / 8
    # NSDate *_userSuppliedMinimumDate                                      180 = 0xb4 / 4          344 = 0x158 / 8
    # NSDate *_userSuppliedMaximumDate                                      184 = 0xb8 / 4          352 = 0x160 / 8
    # NSLocale *_compositeLocale                                            188 = 0xbc / 4          360 = 0x168 / 8
    # NSLocale *_userProvidedLocale                                         192 = 0xc0 / 4          368 = 0x170 / 8
    # NSCalendar *_userProvidedCalendar                                     196 = 0xc4 / 4          376 = 0x178 / 8
    # NSDate *_minimumDate                                                  200 = 0xc8 / 4          384 = 0x180 / 8
    # NSDate *_maximumDate                                                  204 = 0xcc / 4          392 = 0x188 / 8
    # NSDateComponents *_lastSelectedDateComponents                         208 = 0xd0 / 4          400 = 0x190 / 8
    # BOOL _allowsZeroTimeInterval                                          212 = 0xd4 / 1 + 3      408 = 0x198 / 1 + 7
    # _UIDatePickerMode *_mode                                              216 = 0xd8 / 4          416 = 0x1a0 / 8
    # NSTimeZone *_timeZone                                                 220 = 0xdc / 4          424 = 0x1a8 / 8
    # double _timeInterval                                                  224 = 0xe0 / 8          432 = 0x1b0 / 8
    # UILabel *_hourLabel                                                   232 = 0xe8 / 4          440 = 0x1b8 / 8
    # UILabel *_minuteLabel                                                 236 = 0xee / 4          448 = 0x1c0 / 8
    # UIDatePicker *_datePickerDelegate                                     240 = 0xf0 / 4          456 = 0x1c8 / 8
    # id _delegateOfDatePicker                                              244 = 0xf4 / 4          464 = 0x1d0 / 8
    # int _expectedAMPM                                                     248 = 0xf8 / 4          472 = 0x1d8 / 4
    # struct {
    #     unsigned int staggerTimeIntervals:1;
    #     unsigned int loadingDateOrTime:1;
    #     unsigned int highlightsToday:1;
    #     unsigned int usesBlackChrome:1;
    # } _datePickerFlags                                                    252 = 0xfc / 1 + 3      476 = 0x1dc / 1 + 3

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UIDatePickerView_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.date = None
        self.min_user_date = None
        self.max_user_date = None
        self.min_date = None
        self.max_date = None

        self.update()

    def update(self):
        self.date = None
        self.min_user_date = None
        self.max_user_date = None
        self.min_date = None
        self.max_date = None
        super(UIDatePickerView_SynthProvider, self).update()

    def get_date(self):
        if self.date:
            return self.date

        if self.sys_params.is_64_bit:
            offset = 0x150
        else:
            offset = 0xb0

        self.date = self.value_obj.CreateChildAtOffset("date",
                                                       offset,
                                                       self.sys_params.types_cache.NSDate)
        return self.date

    def get_min_user_date(self):
        if self.min_user_date:
            return self.min_user_date

        if self.sys_params.is_64_bit:
            offset = 0x158
        else:
            offset = 0xb4

        self.min_user_date = self.value_obj.CreateChildAtOffset("userSuppliedMinimumDate",
                                                                offset,
                                                                self.sys_params.types_cache.NSDate)
        return self.min_user_date

    def get_max_user_date(self):
        if self.max_user_date:
            return self.max_user_date

        if self.sys_params.is_64_bit:
            offset = 0x160
        else:
            offset = 0xb8

        self.max_user_date = self.value_obj.CreateChildAtOffset("userSuppliedMaximumDate",
                                                                offset,
                                                                self.sys_params.types_cache.NSDate)
        return self.max_user_date

    def get_min_date(self):
        if self.min_date:
            return self.min_date

        if self.sys_params.is_64_bit:
            offset = 0x180
        else:
            offset = 0xc8

        self.min_date = self.value_obj.CreateChildAtOffset("minimumDate",
                                                           offset,
                                                           self.sys_params.types_cache.NSDate)
        return self.min_date

    def get_max_date(self):
        if self.max_date:
            return self.max_date

        if self.sys_params.is_64_bit:
            offset = 0x188
        else:
            offset = 0xcc

        self.max_date = self.value_obj.CreateChildAtOffset("maximumDate",
                                                           offset,
                                                           self.sys_params.types_cache.NSDate)
        return self.max_date

    def summary(self):
        date = self.get_date()
        date_value = date.GetSummary()
        date_summary = "date={}".format(date_value)

        # min_user_date = self.get_min_user_date()
        # min_user_date_value = min_user_date.GetSummary()
        # min_user_date_summary = "minDate={}".format(min_user_date_value)

        # max_user_date = self.get_max_user_date()
        # max_user_date_value = max_user_date.GetSummary()
        # max_user_date_summary = "maxDate={}".format(max_user_date_value)

        # min_date = self.get_min_date()
        # min_date_value = min_date.GetSummary()
        # max_date_summary = "minDate={}".format(min_date_value)

        # max_date = self.get_max_date()
        # max_date_value = max_date.GetSummary()
        # max_date_summary = "maxDate={}".format(max_date_value)

        # Summaries
        summaries = []
        if date_value:
            summaries.append(date_summary)
        # if min_user_date_value:
        #     summaries.append(min_user_date_summary)
        # if max_user_date_value:
        #     summaries.append(max_user_date_summary)

        summary = ", ".join(summaries)
        return summary


def UIDatePickerView_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIDatePickerView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIDatePickerView.UIDatePickerView_SummaryProvider \
                            --category UIKit \
                            _UIDatePickerView")
    debugger.HandleCommand("type category enable UIKit")
