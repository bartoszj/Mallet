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
import NSObject


class UIScreen_SynthProvider(NSObject.NSObject_SynthProvider):
    # UIScreen:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
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
    # } _screenFlags                                                        60 = 0x3c / 2 (+ 2)     112 = 0x70 / 2 + 2
    # BOOL _wantsSoftwareDimming                                            62 = 0x3e / 1 + 1       116 = 0x74 / 1 + 3
    # UISoftwareDimmingWindow *_softwareDimmingWindow                       64 = 0x40 / 4           120 = 0x78 / 8
    # NSInteger _lastNotifiedBacklightLevel                                 68 = 0x44 / 4           128 = 0x80 / 8

    def __init__(self, value_obj, internal_dict):
        super(UIScreen_SynthProvider, self).__init__(value_obj, internal_dict)

        self.bounds = None
        self.scale = None
        self.horizontal_scale = None
        self.interface_idiom = None
        
    def get_bounds(self):
        if self.bounds:
            return self.bounds

        self.bounds = self.get_child_value("_bounds")
        return self.bounds

    def get_scale(self):
        if self.scale:
            return self.scale

        self.scale = self.get_child_value("_scale")
        return self.scale

    def get_horizontal_scale(self):
        if self.horizontal_scale:
            return self.horizontal_scale

        self.horizontal_scale = self.get_child_value("_horizontalScale")
        return self.horizontal_scale

    def get_interface_idiom(self):
        if self.interface_idiom:
            return self.interface_idiom

        self.interface_idiom = self.get_child_value("_userInterfaceIdiom")
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
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIScreen_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIScreen.UIScreen_SummaryProvider \
                            --category UIKit \
                            UIScreen")
    debugger.HandleCommand("type category enable UIKit")
