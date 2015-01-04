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

import NSObject
import Helpers
import SummaryBase


class NSDateComponentsSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSDateComponents.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSDateComponentsSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSDateComponents"

        if self.is_64bit:
            era_offset = 0x18
            year_offset = 0x20
            month_offset = 0x28
            day_offset = 0x30
            hour_offset = 0x38
            minute_offset = 0x40
            second_offset = 0x48
            week_offset = 0x50
            weekday_offset = 0x58
            weekday_ordinal_offset = 0x60
            quarter_offset = 0x68
            week_of_year_offset = 0x78
            week_of_month_offset = 0x80
            year_for_week_of_year_offset = 0x88
            leap_month_offset = 0x90
        else:
            era_offset = 0x0c
            year_offset = 0x10
            month_offset = 0x14
            day_offset = 0x18
            hour_offset = 0x1c
            minute_offset = 0x20
            second_offset = 0x24
            week_offset = 0x28
            weekday_offset = 0x2c
            weekday_ordinal_offset = 0x30
            quarter_offset = 0x38
            week_of_year_offset = 0x3c
            week_of_month_offset = 0x40
            year_for_week_of_year_offset = 0x44
            leap_month_offset = 0x48

        self.register_child_value("era", ivar_name="era", type_name="NSInteger", offset=era_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_era_summary)
        self.register_child_value("year", ivar_name="year", type_name="NSInteger", offset=year_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_year_summary)
        self.register_child_value("month", ivar_name="month", type_name="NSInteger", offset=month_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_month_summary)
        self.register_child_value("day", ivar_name="day", type_name="NSInteger", offset=day_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_day_summary)
        self.register_child_value("hour", ivar_name="hour", type_name="NSInteger", offset=hour_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_hour_summary)
        self.register_child_value("minute", ivar_name="minute", type_name="NSInteger", offset=minute_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_minute_summary)
        self.register_child_value("second", ivar_name="second", type_name="NSInteger", offset=second_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_second_summary)
        self.register_child_value("week", ivar_name="week", type_name="NSInteger", offset=week_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_week_summary)
        self.register_child_value("weekday", ivar_name="weekday", type_name="NSInteger", offset=weekday_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_weekday_summary)
        self.register_child_value("weekday_ordinal", ivar_name="weekday_ordinal", type_name="NSInteger", offset=weekday_ordinal_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_weekday_ordinal_summary)
        self.register_child_value("quarter", ivar_name="quarter", type_name="NSInteger", offset=quarter_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_quarter_summary)
        self.register_child_value("week_of_year", ivar_name="week_of_year", type_name="NSInteger", offset=week_of_year_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_week_of_year_summary)
        self.register_child_value("week_of_month", ivar_name="week_of_month", type_name="NSInteger", offset=week_of_month_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_week_of_month_summary)
        self.register_child_value("year_for_week_of_year", ivar_name="year_for_week_of_year", type_name="NSInteger", offset=year_for_week_of_year_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_year_for_week_of_year_summary)
        self.register_child_value("leap_month", ivar_name="leap_month", type_name="NSInteger", offset=leap_month_offset,
                                  primitive_value_function=self.get_signed_not_empty_value,
                                  summary_function=self.get_leap_month_summary)

    def get_signed_not_empty_value(self, obj):
        """
        Returns signed integer from LLDB value if it is not equal to 0x7FFFFFFFFFFFFFFF or 0x7FFFFFFF.

        :param lldb.SBValue obj: LLDB value object.
        :return: Signed integer from LLDB value.
        :rtype: int | None
        """
        value = SummaryBase.get_signed_value(obj)
        if value is None:
            return None

        if self.is_not_empty_value(value):
            return value
        return None

    def is_not_empty_value(self, value):
        """
        Returns True if value is different than 0x7FFFFFFFFFFFFFFF or 0x7FFFFFFF.

        :param int value: Value
        :return: True if value is not 'empty'.
        :rtype: bool
        """
        if self.is_64bit and value == 0x7FFFFFFFFFFFFFFF:
            return False
        elif not self.is_64bit and value == 0x7FFFFFFF:
            return False
        return True

    @staticmethod
    def get_era_summary(value):
        return "era={}".format(value)

    @staticmethod
    def get_year_summary(value):
        return "year={}".format(value)

    @staticmethod
    def get_month_summary(value):
        return "month={}".format(value)

    @staticmethod
    def get_day_summary(value):
        return "day={}".format(value)

    @staticmethod
    def get_hour_summary(value):
        return "hour={}".format(value)

    @staticmethod
    def get_minute_summary(value):
        return "minute={}".format(value)

    @staticmethod
    def get_second_summary(value):
        return "second={}".format(value)

    @staticmethod
    def get_week_summary(value):
        return "week={}".format(value)

    @staticmethod
    def get_weekday_summary(value):
        return "weekday={}".format(value)

    @staticmethod
    def get_weekday_ordinal_summary(value):
        return "weekdayOrdinal={}".format(value)

    @staticmethod
    def get_quarter_summary(value):
        return "quarter={}".format(value)

    @staticmethod
    def get_week_of_year_summary(value):
        return "weekOfYear={}".format(value)

    @staticmethod
    def get_week_of_month_summary(value):
        return "weekOfMonth={}".format(value)

    @staticmethod
    def get_year_for_week_of_year_summary(value):
        return "yearForWeekOfYear={}".format(value)

    @staticmethod
    def get_leap_month_summary(value):
        if value != 0:
            return "leapMonth=YES"
        else:
            return "leapMonth=NO"

    def summary(self):
        year_value = self.year_value
        month_value = self.month_value
        day_value = self.day_value
        hour_value = self.hour_value
        minute_value = self.minute_value
        second_value = self.second_value

        # Date in ISO format.
        iso_date_summary = None
        date_summary = None
        time_summary = None

        if year_value is not None and \
           month_value is not None and \
           day_value is not None and \
           hour_value is not None and \
           minute_value is not None:
            if second_value is not None:
                # YYYY-MM-dd HH:mm:ss
                iso_date_summary = "{}-{:02}-{:02} {:02}:{:02}:{:02}".format(year_value, month_value, day_value,
                                                                             hour_value, minute_value, second_value)
            else:
                # YYYY-MM-dd HH:mm
                iso_date_summary = "{}-{:02}-{:02} {:02}:{:02}".format(year_value, month_value, day_value,
                                                                       hour_value, minute_value)
        else:
            if year_value is not None and \
               month_value is not None and \
               day_value is not None:
                # YYYY-MM-dd
                date_summary = "date={}-{:02}-{:02}".format(year_value, month_value, day_value)

            if hour_value is not None and \
               minute_value is not None:
                if second_value is not None:
                    # HH:mm:ss
                    time_summary = "time={:02}:{:02}:{:02}".format(hour_value, minute_value, second_value)
                else:
                    # HH:mm
                    time_summary = "time={:02}:{:02}".format(hour_value, minute_value)

        # Summaries
        summaries = [self.era_summary, iso_date_summary, date_summary, time_summary]
        if iso_date_summary is None:
            if date_summary is None:
                summaries.extend([self.year_summary, self.month_summary, self.day_summary])
            if time_summary is None:
                summaries.extend([self.hour_summary, self.minute_summary, self.second_summary])
        summaries.extend([self.week_summary, self.weekday_summary, self.weekday_ordinal_summary,
                          self.quarter_summary, self.week_of_year_summary, self.week_of_month_summary,
                          self.year_for_week_of_year_summary, self.leap_month_summary])

        summary = SummaryBase.join_summaries(*summaries)
        return summary


def summary_provider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, NSDateComponentsSyntheticProvider)


def __lldb_init_module(debugger, dictionary):
    debugger.HandleCommand("type summary add -F NSDateComponents.summary_provider \
                            --category Foundation \
                            NSDateComponents")
    debugger.HandleCommand("type category enable Foundation")
