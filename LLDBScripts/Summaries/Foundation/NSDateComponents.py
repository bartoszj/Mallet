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
import NSObject


class NSDateComponents_SynthProvider(NSObject.NSObject_SynthProvider):
    # NSDateComponents:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSCalendar *calendar                                                    4 = 0x04 / 4            8 = 0x08 / 8
    # NSTimeZone *timeZone                                                    8 = 0x08 / 4           16 = 0x10 / 8
    # NSInteger era                                                          12 = 0x0c / 4           24 = 0x18 / 8
    # NSInteger year                                                         16 = 0x10 / 4           32 = 0x20 / 8
    # NSInteger month                                                        20 = 0x14 / 4           40 = 0x28 / 8
    # NSInteger day                                                          24 = 0x18 / 4           48 = 0x30 / 8
    # NSInteger hour                                                         28 = 0x1c / 4           56 = 0x38 / 8
    # NSInteger minute                                                       32 = 0x20 / 4           64 = 0x40 / 8
    # NSInteger seconds                                                      36 = 0x24 / 4           72 = 0x48 / 8
    # NSInteger week                                                         40 = 0x28 / 4           80 = 0x50 / 8
    # NSInteger weekday                                                      44 = 0x2c / 4           88 = 0x58 / 8
    # NSInteger weekdayOrdinal                                               48 = 0x30 / 4           96 = 0x60 / 8
    # NSInteger quarter                                                      52 = 0x34 / 4          104 = 0x68 / 8
    # id ?                                                                   56 = 0x38 / 4          112 = 0x70 / 8
    # NSInteger weekOfYear                                                   60 = 0x3c / 4          120 = 0x78 / 8
    # NSInteger weekOfMonth                                                  64 = 0x40 / 4          128 = 0x80 / 8
    # NSInteger yearForWeekOfYear                                            68 = 0x44 / 4          136 = 0x88 / 8
    # NSInteger leapMonth                                                    72 = 0x48 / 4          144 = 0x90 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(NSDateComponents_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

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

        self.update()

    def update(self):
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
        super(NSDateComponents_SynthProvider, self).update()

    def is_not_empty_value(self, value):
        if self.sys_params.is_64_bit and value == 0x7FFFFFFFFFFFFFFF:
            return False
        elif not self.sys_params.is_64_bit and value == 0x7FFFFFFF:
            return False
        return True

    def get_era(self):
        if self.era:
            return self.era

        if self.sys_params.is_64_bit:
            offset = 0x18
        else:
            offset = 0x0c

        self.era = self.value_obj.CreateChildAtOffset("era",
                                                      offset,
                                                      self.sys_params.types_cache.NSInteger)
        return self.era

    def get_year(self):
        if self.year:
            return self.year

        if self.sys_params.is_64_bit:
            offset = 0x20
        else:
            offset = 0x10

        self.year = self.value_obj.CreateChildAtOffset("year",
                                                       offset,
                                                       self.sys_params.types_cache.NSInteger)
        return self.year

    def get_month(self):
        if self.month:
            return self.month

        if self.sys_params.is_64_bit:
            offset = 0x28
        else:
            offset = 0x14

        self.month = self.value_obj.CreateChildAtOffset("month",
                                                        offset,
                                                        self.sys_params.types_cache.NSInteger)
        return self.month

    def get_day(self):
        if self.day:
            return self.day

        if self.sys_params.is_64_bit:
            offset = 0x30
        else:
            offset = 0x18

        self.day = self.value_obj.CreateChildAtOffset("day",
                                                      offset,
                                                      self.sys_params.types_cache.NSInteger)
        return self.day

    def get_hour(self):
        if self.hour:
            return self.hour

        if self.sys_params.is_64_bit:
            offset = 0x38
        else:
            offset = 0x1c

        self.hour = self.value_obj.CreateChildAtOffset("hour",
                                                       offset,
                                                       self.sys_params.types_cache.NSInteger)
        return self.hour

    def get_minute(self):
        if self.minute:
            return self.minute

        if self.sys_params.is_64_bit:
            offset = 0x40
        else:
            offset = 0x20

        self.minute = self.value_obj.CreateChildAtOffset("minute",
                                                         offset,
                                                         self.sys_params.types_cache.NSInteger)
        return self.minute

    def get_second(self):
        if self.second:
            return self.second

        if self.sys_params.is_64_bit:
            offset = 0x48
        else:
            offset = 0x24

        self.second = self.value_obj.CreateChildAtOffset("second",
                                                         offset,
                                                         self.sys_params.types_cache.NSInteger)
        return self.second

    def get_week(self):
        if self.week:
            return self.week

        if self.sys_params.is_64_bit:
            offset = 0x50
        else:
            offset = 0x28

        self.week = self.value_obj.CreateChildAtOffset("week",
                                                       offset,
                                                       self.sys_params.types_cache.NSInteger)
        return self.week

    def get_weekday(self):
        if self.weekday:
            return self.weekday

        if self.sys_params.is_64_bit:
            offset = 0x58
        else:
            offset = 0x2c

        self.weekday = self.value_obj.CreateChildAtOffset("weekday",
                                                          offset,
                                                          self.sys_params.types_cache.NSInteger)
        return self.weekday

    def get_weekday_ordinal(self):
        if self.weekday_ordinal:
            return self.weekday_ordinal

        if self.sys_params.is_64_bit:
            offset = 0x60
        else:
            offset = 0x30

        self.weekday_ordinal = self.value_obj.CreateChildAtOffset("weekday_ordinal",
                                                                  offset,
                                                                  self.sys_params.types_cache.NSInteger)
        return self.weekday_ordinal

    def get_quarter(self):
        if self.quarter:
            return self.quarter

        if self.sys_params.is_64_bit:
            offset = 0x68
        else:
            offset = 0x34

        self.quarter = self.value_obj.CreateChildAtOffset("quarter",
                                                          offset,
                                                          self.sys_params.types_cache.NSInteger)
        return self.quarter

    def get_week_of_year(self):
        if self.week_of_year:
            return self.week_of_year

        if self.sys_params.is_64_bit:
            offset = 0x78
        else:
            offset = 0x3c

        self.week_of_year = self.value_obj.CreateChildAtOffset("week_of_year",
                                                               offset,
                                                               self.sys_params.types_cache.NSInteger)
        return self.week_of_year

    def get_week_of_month(self):
        if self.week_of_month:
            return self.week_of_month

        if self.sys_params.is_64_bit:
            offset = 0x80
        else:
            offset = 0x40

        self.week_of_month = self.value_obj.CreateChildAtOffset("week_of_month",
                                                                offset,
                                                                self.sys_params.types_cache.NSInteger)
        return self.week_of_month

    def get_year_for_week_of_year(self):
        if self.year_for_week_of_year:
            return self.year_for_week_of_year

        if self.sys_params.is_64_bit:
            offset = 0x88
        else:
            offset = 0x44

        self.year_for_week_of_year = self.value_obj.CreateChildAtOffset("year_for_week_of_year",
                                                                        offset,
                                                                        self.sys_params.types_cache.NSInteger)
        return self.year_for_week_of_year

    def get_leap_month(self):
        if self.leap_month:
            return self.leap_month

        if self.sys_params.is_64_bit:
            offset = 0x90
        else:
            offset = 0x48

        self.leap_month = self.value_obj.CreateChildAtOffset("leap_month",
                                                             offset,
                                                             self.sys_params.types_cache.NSInteger)
        return self.leap_month

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
        if self.is_not_empty_value(year_value):
            summaries.append(year_summary)
        if self.is_not_empty_value(month_value):
            summaries.append(month_summary)
        if self.is_not_empty_value(day_value):
            summaries.append(day_summary)
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
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, NSDateComponents_SynthProvider,
                                                   ["NSDateComponents"])


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F NSDateComponents.NSDateComponents_SummaryProvider \
                            --category Foundation \
                            NSDateComponents")
    debugger.HandleCommand("type category enable Foundation")
