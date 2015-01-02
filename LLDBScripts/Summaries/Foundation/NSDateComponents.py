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


class NSDateComponents_SynthProvider(NSObject.NSObject_SynthProvider):
    def __init__(self, value_obj, internal_dict):
        super(NSDateComponents_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSDateComponents"

        self.era = None
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None
        self.week = None
        self.weekday = None
        self.weekday_ordinal = None
        self.quarter = None
        self.week_of_year = None
        self.week_of_month = None
        self.year_for_week_of_year = None
        self.leap_month = None

    def is_not_empty_value(self, value):
        if self.is_64bit and value == 0x7FFFFFFFFFFFFFFF:
            return False
        elif not self.is_64bit and value == 0x7FFFFFFF:
            return False
        return True

    @Helpers.save_parameter("era")
    def get_era(self):
        if self.is_64bit:
            offset = 0x18
        else:
            offset = 0x0c

        return self.get_child_value("era", "NSInteger", offset)

    @Helpers.save_parameter("year")
    def get_year(self):
        if self.is_64bit:
            offset = 0x20
        else:
            offset = 0x10

        return self.get_child_value("year", "NSInteger", offset)

    @Helpers.save_parameter("month")
    def get_month(self):
        if self.is_64bit:
            offset = 0x28
        else:
            offset = 0x14

        return self.get_child_value("month", "NSInteger", offset)

    @Helpers.save_parameter("day")
    def get_day(self):
        if self.is_64bit:
            offset = 0x30
        else:
            offset = 0x18

        return self.get_child_value("day", "NSInteger", offset)

    @Helpers.save_parameter("hour")
    def get_hour(self):
        if self.is_64bit:
            offset = 0x38
        else:
            offset = 0x1c

        return self.get_child_value("hour", "NSInteger", offset)

    @Helpers.save_parameter("minute")
    def get_minute(self):
        if self.is_64bit:
            offset = 0x40
        else:
            offset = 0x20

        return self.get_child_value("minute", "NSInteger", offset)

    @Helpers.save_parameter("second")
    def get_second(self):
        if self.is_64bit:
            offset = 0x48
        else:
            offset = 0x24

        return self.get_child_value("second", "NSInteger", offset)

    @Helpers.save_parameter("week")
    def get_week(self):
        if self.is_64bit:
            offset = 0x50
        else:
            offset = 0x28

        return self.get_child_value("week", "NSInteger", offset)

    @Helpers.save_parameter("weekday")
    def get_weekday(self):
        if self.is_64bit:
            offset = 0x58
        else:
            offset = 0x2c

        return self.get_child_value("weekday", "NSInteger", offset)

    @Helpers.save_parameter("weekday_ordinal")
    def get_weekday_ordinal(self):
        if self.is_64bit:
            offset = 0x60
        else:
            offset = 0x30

        return self.get_child_value("weekday_ordinal", "NSInteger", offset)

    @Helpers.save_parameter("quarter")
    def get_quarter(self):
        if self.is_64bit:
            offset = 0x68
        else:
            offset = 0x34

        return self.get_child_value("quarter", "NSInteger", offset)

    @Helpers.save_parameter("week_of_year")
    def get_week_of_year(self):
        if self.is_64bit:
            offset = 0x78
        else:
            offset = 0x3c

        return self.get_child_value("week_of_year", "NSInteger", offset)

    @Helpers.save_parameter("week_of_month")
    def get_week_of_month(self):
        if self.is_64bit:
            offset = 0x80
        else:
            offset = 0x40

        return self.get_child_value("week_of_month", "NSInteger", offset)

    @Helpers.save_parameter("year_for_week_of_year")
    def get_year_for_week_of_year(self):
        if self.is_64bit:
            offset = 0x88
        else:
            offset = 0x44

        return self.get_child_value("year_of_week_of_year", "NSInteger", offset)

    @Helpers.save_parameter("leap_month")
    def get_leap_month(self):
        if self.is_64bit:
            offset = 0x90
        else:
            offset = 0x48

        return self.get_child_value("leap_month", "NSInteger", offset)

    def summary(self):
        era = self.get_era()
        era_value = era.GetValueAsSigned()
        era_summary = "era={}".format(era_value)

        year = self.get_year()
        year_value = year.GetValueAsSigned()
        year_summary = "year={}".format(year_value)

        month = self.get_month()
        month_value = month.GetValueAsSigned()
        month_summary = "month={}".format(month_value)

        day = self.get_day()
        day_value = day.GetValueAsSigned()
        day_summary = "day={}".format(day_value)

        hour = self.get_hour()
        hour_value = hour.GetValueAsSigned()
        hour_summary = "hour={}".format(hour_value)

        minute = self.get_minute()
        minute_value = minute.GetValueAsSigned()
        minute_summary = "minute={}".format(minute_value)

        second = self.get_second()
        second_value = second.GetValueAsSigned()
        second_summary = "second={}".format(second_value)

        # Date in ISO format.
        if self.is_not_empty_value(year_value) and \
           self.is_not_empty_value(month_value) and \
           self.is_not_empty_value(day_value) and \
           self.is_not_empty_value(hour_value) and \
           self.is_not_empty_value(minute_value):
            if self.is_not_empty_value(second_value):
                # YYYY-MM-dd HH:mm:ss
                date_summary = "{}-{:02}-{:02} {:02}:{:02}:{:02}".format(year_value, month_value, day_value,
                                                                         hour_value, minute_value, second_value)
            else:
                # YYYY-MM-dd HH:mm
                date_summary = "{}-{:02}-{:02} {:02}:{:02}".format(year_value, month_value, day_value,
                                                                   hour_value, minute_value)
        else:
            if self.is_not_empty_value(year_value) and \
               self.is_not_empty_value(month_value) and \
               self.is_not_empty_value(day_value):
                # YYYY-MM-dd
                date_summary = "date={}-{:02}-{:02}".format(year_value, month_value, day_value)

            if self.is_not_empty_value(hour_value) and \
               self.is_not_empty_value(minute_value):
                if self.is_not_empty_value(second_value):
                    # HH:mm:ss
                    time_summary = "time={:02}:{:02}:{:02}".format(hour_value, minute_value, second_value)
                else:
                    # HH:mm
                    time_summary = "time={:02}:{:02}".format(hour_value, minute_value)

        week = self.get_week()
        week_value = week.GetValueAsSigned()
        week_summary = "week={}".format(week_value)

        weekday = self.get_weekday()
        weekday_value = weekday.GetValueAsSigned()
        weekday_summary = "weekday={}".format(weekday_value)

        weekday_ordinal = self.get_weekday_ordinal()
        weekday_ordinal_value = weekday_ordinal.GetValueAsSigned()
        weekday_ordinal_summary = "weekdayOrdinal={}".format(weekday_ordinal_value)

        quarter = self.get_quarter()
        quarter_value = quarter.GetValueAsSigned()
        quarter_summary = "quarter={}".format(quarter_value)

        week_of_year = self.get_week_of_year()
        week_of_year_value = week_of_year.GetValueAsSigned()
        week_of_year_summary = "weekOfYear={}".format(week_of_year_value)

        week_of_month = self.get_week_of_month()
        week_of_month_value = week_of_month.GetValueAsSigned()
        week_of_month_summary = "weekOfMonth={}".format(week_of_month_value)

        year_for_week_of_year = self.get_year_for_week_of_year()
        year_for_week_of_year_value = year_for_week_of_year.GetValueAsSigned()
        year_for_week_of_year_summary = "yearForWeekOfYear={}".format(year_for_week_of_year_value)

        leap_month = self.get_leap_month()
        leap_month_value = leap_month.GetValueAsSigned()
        leap_month_summary = "leapMonth={}".format(format("YES" if leap_month_value != 0 else "NO"))

        # Summaries
        summaries = []
        if self.is_not_empty_value(era_value):
            summaries.append(era_summary)

        if self.is_not_empty_value(year_value) and \
           self.is_not_empty_value(month_value) and \
           self.is_not_empty_value(day_value) and \
           self.is_not_empty_value(hour_value) and \
           self.is_not_empty_value(minute_value):
            summaries.append(date_summary)
        else:
            if self.is_not_empty_value(year_value) and \
               self.is_not_empty_value(month_value) and \
               self.is_not_empty_value(day_value):
                summaries.append(date_summary)
            else:
                if self.is_not_empty_value(year_value):
                    summaries.append(year_summary)
                if self.is_not_empty_value(month_value):
                    summaries.append(month_summary)
                if self.is_not_empty_value(day_value):
                    summaries.append(day_summary)

            if self.is_not_empty_value(hour_value) and \
               self.is_not_empty_value(minute_value):
                summaries.append(time_summary)
            else:
                if self.is_not_empty_value(hour_value):
                    summaries.append(hour_summary)
                if self.is_not_empty_value(minute_value):
                    summaries.append(minute_summary)
                if self.is_not_empty_value(second_value):
                    summaries.append(second_summary)
        if self.is_not_empty_value(week_value):
            summaries.append(week_summary)
        if self.is_not_empty_value(weekday_value):
            summaries.append(weekday_summary)
        if self.is_not_empty_value(weekday_ordinal_value):
            summaries.append(weekday_ordinal_summary)
        if self.is_not_empty_value(quarter_value):
            summaries.append(quarter_summary)
        if self.is_not_empty_value(week_of_year_value):
            summaries.append(week_of_year_summary)
        if self.is_not_empty_value(week_of_month_value):
            summaries.append(week_of_month_summary)
        if self.is_not_empty_value(year_for_week_of_year_value):
            summaries.append(year_for_week_of_year_summary)
        if self.is_not_empty_value(leap_month_value):
            summaries.append(leap_month_summary)

        summary = ", ".join(summaries)
        return summary


def NSDateComponents_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, NSDateComponents_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F NSDateComponents.NSDateComponents_SummaryProvider \
                            --category Foundation \
                            NSDateComponents")
    debugger.HandleCommand("type category enable Foundation")
