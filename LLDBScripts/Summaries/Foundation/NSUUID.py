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
import Helpers
import NSObject


class NSUUID_SynthProvider(NSObject.NSObjectSyntheticProvider):
    def __init__(self, value_obj, internal_dict):
        super(NSUUID_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "NSUUID"

        self.uuid = None

    @Helpers.save_parameter("uuid")
    def get_uuid(self):
        if self.is_64bit:
            offset = 8
        else:
            offset = 4

        return self.get_child_value("uuid", "uuid_t", offset)

    def get_uuid_data(self):
        uuid = self.get_uuid()
        if uuid is None:
            return None
        uuid_data = self.get_uuid().GetData()
        uuid_data.SetByteOrder(lldb.eByteOrderBig)
        return uuid_data

    def get_uuid_summary(self):
        uuid_data = self.get_uuid_data()
        if uuid_data is None:
            return None
        error = lldb.SBError()
        return "{:08X}-{:04X}-{:04X}-{:04X}-{:08X}{:04X}".format(uuid_data.GetUnsignedInt32(error, 0),
                                                                 uuid_data.GetUnsignedInt16(error, 4),
                                                                 uuid_data.GetUnsignedInt16(error, 6),
                                                                 uuid_data.GetUnsignedInt16(error, 8),
                                                                 uuid_data.GetUnsignedInt32(error, 10),
                                                                 uuid_data.GetUnsignedInt16(error, 14))

    def summary(self):
        uuid_summary = self.get_uuid_summary()

        return uuid_summary


def NSUUID_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, NSUUID_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F NSUUID.NSUUID_SummaryProvider \
                            --category Foundation \
                            NSUUID __NSConcreteUUID")
    debugger.HandleCommand("type category enable Foundation")
