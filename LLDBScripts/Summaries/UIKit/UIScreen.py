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


class UIScreen_SynthProvider(NSObject.NSObject_SynthProvider):
    # UIScreen:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # Class isa                                                               0 = 0x00 / 4            0 = 0x00 / 8
    # id _display                                                             4 = 0x04 / 4            8 = 0x08 / 8
    # CGRect _bounds                                                          8 = 0x08 / 16          16 = 0x10 / 32
    # CGFloat _scale                                                         24 = 0x18 / 4           48 = 0x30 / 8
    # CGFloat _horizontalScale                                               28 = 0x1c / 4           56 = 0x38 / 8
    # NSInteger _userInterfaceIdiom                                          32 = 0x20 / 4           64 = 0x40 / 8
    # NSDictionary *_capabilities                                            36 = 0x24 / 4           72 = 0x48 / 8
    # NSInteger _workspaceCapableScreenType                                  40 = 0x28 / 4           80 = 0x50 / 8
    # UIWindow *_screenDisablingWindow                                       44 = 0x2c / 4           88 = 0x58 / 8
    # double _startedPausingWindows                                          48 = 0x30 / 8           96 = 0x60 / 8
    # NSMutableArray *_pausedWindows                                         56 = 0x38 / 4          104 = 0x68 / 8
    # struct {
    #     unsigned bitsPerComponent : 4
    #     unsigned initialized : 1
    #     unsigned connected : 1
    #     unsigned overscanCompensation : 2
    #     unsigned hasShownWindows : 1
    #     unsigned canAccessDisplay : 1
    #     unsigned canAccessDisplayValid : 1
    #     unsigned screenUpdatesDisabled : 1
    # } _screenFlags                                                        60 = 0x3c / 2           112 = 0x70 / 2
    # BOOL _wantsSoftwareDimming                                            62 = 0x3e / 1 + 1       114 = 0x72 / 1 + 5
    # UISoftwareDimmingWindow *_softwareDimmingWindow                       64 = 0x40 / 4           120 = 0x78 / 8
    # NSInteger _lastNotifiedBacklightLevel                                 68 = 0x44 / 4           128 = 0x80 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        super(UIScreen_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.bounds = None
        self.scale = None
        self.horizontal_scale = None
        self.interface_idiom = None
        
        self.update()

    def update(self):
        self.bounds = None
        self.scale = None
        self.horizontal_scale = None
        self.interface_idiom = None
        super(UIScreen_SynthProvider, self).update()

    def get_bounds(self):
        if self.bounds:
            return self.bounds

        self.bounds = self.value_obj.CreateChildAtOffset("bounds",
                                                         2 * self.sys_params.pointer_size,
                                                         self.sys_params.types_cache.CGRect)
        return self.bounds

    def get_scale(self):
        if self.scale:
            return self.scale

        if self.sys_params.is_64_bit:
            offset = 0x30
        else:
            offset = 0x18

        self.scale = self.value_obj.CreateChildAtOffset("scale",
                                                        offset,
                                                        self.sys_params.types_cache.CGFloat)
        return self.scale

    def get_horizontal_scale(self):
        if self.horizontal_scale:
            return self.horizontal_scale

        if self.sys_params.is_64_bit:
            offset = 0x38
        else:
            offset = 0x1c

        self.horizontal_scale = self.value_obj.CreateChildAtOffset("horizontalScale",
                                                                   offset,
                                                                   self.sys_params.types_cache.CGFloat)
        return self.horizontal_scale

    def get_interface_idiom(self):
        if self.interface_idiom:
            return self.interface_idiom

        if self.sys_params.is_64_bit:
            offset = 0x40
        else:
            offset = 0x20

        self.interface_idiom = self.value_obj.CreateChildAtOffset("interfaceIdiom",
                                                                  offset,
                                                                  self.sys_params.types_cache.int)
        return self.interface_idiom

    def summary(self):
        bounds = self.get_bounds()
        size = bounds.GetChildMemberWithName("size")
        w = float(size.GetChildMemberWithName("width").GetValue())
        h = float(size.GetChildMemberWithName("height").GetValue())
        bounds_summary = "size=({:.0f}, {:.0f})".format(w, h)

        scale = self.get_scale()
        scale_summary = "scale={:.1f}".format(float(scale.GetValue()))

        # horizontal_scale = self.get_horizontal_scale()
        # horizontal_scale_summary = "hScale={:.0f}".format(float(horizontal_scale.GetValue()))

        interface_idiom_value = self.get_interface_idiom().GetValueAsSigned()
        interface_idiom_name = "Unknown"
        if interface_idiom_value == 0:
            interface_idiom_name = "Phone"
        elif interface_idiom_value == 1:
            interface_idiom_name = "Pad"
        interface_idiom_summary = "idiom={}".format(interface_idiom_name)

        # Summaries
        summaries = [bounds_summary, scale_summary, interface_idiom_summary]
        summary = ", ".join(summaries)
        return summary


def UIScreen_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIScreen_SynthProvider,
                                                   ["UIScreen"])


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIScreen.UIScreen_SummaryProvider \
                            --category UIKit \
                            UIScreen")
    debugger.HandleCommand("type category enable UIKit")
