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


class NSUUID_SynthProvider(NSObject.NSObject_SynthProvider):
    # NSUUID:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # uuid_t/unsigned char[16]                                                4 = 0x04 / 16           8 = 0x08 / 16

    def __init__(self, value_obj, sys_params, internal_dict):
        super(NSUUID_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.uuid_data = None

        self.update()

    def update(self):
        self.uuid_data = None
        super(NSUUID_SynthProvider, self).update()

    def get_uuid(self):
        if self.uuid_data:
            return self.uuid_data

        if self.sys_params.is_64_bit:
            self.uuid_data = self.value_obj.CreateChildAtOffset("uuid", 8, self.sys_params.types_cache.uuid_t)
        else:
            self.uuid_data = self.value_obj.CreateChildAtOffset("uuid", 4, self.sys_params.types_cache.uuid_t)
        return self.uuid_data

    def summary(self):
        uuid_data = self.get_uuid().GetData()
        uuid_data.SetByteOrder(lldb.eByteOrderBig)

        error = lldb.SBError()
        uuid_summary = "{:08X}-{:04X}-{:04X}-{:04X}-{:08X}{:04X}".format(uuid_data.GetUnsignedInt32(error, 0),
                                                                         uuid_data.GetUnsignedInt16(error, 4),
                                                                         uuid_data.GetUnsignedInt16(error, 6),
                                                                         uuid_data.GetUnsignedInt16(error, 8),
                                                                         uuid_data.GetUnsignedInt32(error, 10),
                                                                         uuid_data.GetUnsignedInt16(error, 14))

        return uuid_summary


def NSUUID_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, NSUUID_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F NSUUID.NSUUID_SummaryProvider \
                            --category Foundation \
                            NSUUID __NSConcreteUUID")
    debugger.HandleCommand("type category enable Foundation")
