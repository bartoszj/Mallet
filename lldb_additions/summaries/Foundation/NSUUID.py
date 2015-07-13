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

from ... import helpers
import lldb
import NSObject


class NSUUIDSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing NSUUID.
    """
    def __init__(self, value_obj, internal_dict):
        super(NSUUIDSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSUUID"

        if self.is_64bit:
            uuid_offset = 8
        else:
            uuid_offset = 4
        self.register_child_value("uuid", ivar_name="uuid", type_name="uuid_t", offset=uuid_offset,
                                  primitive_value_function=self.get_uuid_data,
                                  summary_function=self.get_uuid_summary)

    @staticmethod
    def get_uuid_data(value):
        uuid_data = value.GetData()
        uuid_data.SetByteOrder(lldb.eByteOrderBig)
        return uuid_data

    @staticmethod
    def get_uuid_summary(data):
        error = lldb.SBError()
        return "{:08X}-{:04X}-{:04X}-{:04X}-{:08X}{:04X}".format(data.GetUnsignedInt32(error, 0),
                                                                 data.GetUnsignedInt16(error, 4),
                                                                 data.GetUnsignedInt16(error, 6),
                                                                 data.GetUnsignedInt16(error, 8),
                                                                 data.GetUnsignedInt32(error, 10),
                                                                 data.GetUnsignedInt16(error, 14))

    def summaries_parts(self):
        return [self.uuid_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, NSUUIDSyntheticProvider)
