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
import CGRect


class UIScreen_SynthProvider(NSObject.NSObject_SynthProvider):
    # Class: UIScreen
    # Super class: NSObject
    # Name:                                                 armv7                 i386                  arm64                 x86_64
    # id _display                                         4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # CGRect _bounds                                      8 (0x008) / 16        8 (0x008) / 16       16 (0x010) / 32       16 (0x010) / 32
    # CGFloat _scale                                     24 (0x018) / 4        24 (0x018) / 4        48 (0x030) / 8        48 (0x030) / 8
    # CGFloat _horizontalScale                           28 (0x01C) / 4        28 (0x01C) / 4        56 (0x038) / 8        56 (0x038) / 8
    # NSInteger _userInterfaceIdiom                      32 (0x020) / 4        32 (0x020) / 4        64 (0x040) / 8        64 (0x040) / 8
    # NSDictionary * _capabilities                       36 (0x024) / 4        36 (0x024) / 4        72 (0x048) / 8        72 (0x048) / 8
    # NSInteger _workspaceCapableScreenType              40 (0x028) / 4        40 (0x028) / 4        80 (0x050) / 8        80 (0x050) / 8
    # UIWindow * _screenDisablingWindow                  44 (0x02C) / 4        44 (0x02C) / 4        88 (0x058) / 8        88 (0x058) / 8
    # double _startedPausingWindows                      48 (0x030) / 8        48 (0x030) / 8        96 (0x060) / 8        96 (0x060) / 8
    # NSMutableArray * _pausedWindows                    56 (0x038) / 4        56 (0x038) / 4       104 (0x068) / 8       104 (0x068) / 8
    # NSDictionary * _touchMap                           60 (0x03C) / 4        60 (0x03C) / 4       112 (0x070) / 8       112 (0x070) / 8
    # NSArray * _availableDisplayModes                   64 (0x040) / 4        64 (0x040) / 4       120 (0x078) / 8       120 (0x078) / 8
    # unsigned int _canAccessDisplaySeed                 68 (0x044) / 4        68 (0x044) / 4       128 (0x080) / 4       128 (0x080) / 4
    # unsigned int _connectionSeed                       72 (0x048) / 4        72 (0x048) / 4       132 (0x084) / 4       132 (0x084) / 4
    # struct {
    #         unsigned int bitsPerComponent:4;
    #         unsigned int initialized:1;
    #         unsigned int connected:1;
    #         unsigned int overscanCompensation:2;
    #         unsigned int canAccessDisplay:1;
    #         unsigned int canAccessDisplaySeedValid:1;
    #         unsigned int screenUpdatesDisabled:1;
    #     } _screenFlags                                 76 (0x04C) / 2        76 (0x04C) / 4       136 (0x088) / 4       136 (0x088) / 4
    # BOOL _wantsSoftwareDimming                         78 (0x04E) / 1  + 1   80 (0x050) / 1  + 3  140 (0x08C) / 1  + 3  140 (0x08C) / 1  + 3
    # UISoftwareDimmingWindow * _softwareDimmingWindow   80 (0x050) / 4        84 (0x054) / 4       144 (0x090) / 8       144 (0x090) / 8
    # NSInteger _lastNotifiedBacklightLevel              84 (0x054) / 4        88 (0x058) / 4       152 (0x098) / 8       152 (0x098) / 8

    def __init__(self, value_obj, internal_dict):
        super(UIScreen_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIScreen"

        self.bounds = None
        self.scale = None
        self.horizontal_scale = None
        self.interface_idiom = None

    def get_bounds(self):
        if self.bounds:
            return self.bounds

        self.bounds = self.get_child_value("_bounds")
        return self.bounds

    def get_bounds_provider(self):
        bounds = self.get_bounds()
        return CGRect.CGRect_SynthProvider(bounds, self.internal_dict)

    def get_bounds_summary(self):
        w = self.get_bounds_provider().get_size_provider().get_width_value()
        h = self.get_bounds_provider().get_size_provider().get_height_value()
        return "size=({}, {})".format(self.formatted_float(w), self.formatted_float(h))

    def get_scale(self):
        if self.scale:
            return self.scale

        self.scale = self.get_child_value("_scale")
        return self.scale

    def get_scale_value(self):
        return self.get_float_value(self.get_scale())

    def get_scale_summary(self):
        scale_value = self.get_scale_value()
        if scale_value is None:
            return None
        return "scale={}".format(self.formatted_float(scale_value))

    def get_horizontal_scale(self):
        if self.horizontal_scale:
            return self.horizontal_scale

        self.horizontal_scale = self.get_child_value("_horizontalScale")
        return self.horizontal_scale

    def get_horizontal_scale_value(self):
        return self.get_float_value(self.get_horizontal_scale())

    def get_horizontal_scale_summary(self):
        horizontal_scale_value = self.get_horizontal_scale_value()
        if horizontal_scale_value is None:
            return None
        return "hScale={:.0f}".format(self.formatted_float(horizontal_scale_value))

    def get_interface_idiom(self):
        if self.interface_idiom:
            return self.interface_idiom

        self.interface_idiom = self.get_child_value("_userInterfaceIdiom")
        return self.interface_idiom

    def get_interface_idiom_value(self):
        interface_idiom_value = self.get_interface_idiom().GetValueAsSigned()
        interface_idiom_name = "Unknown"
        if interface_idiom_value == 0:
            interface_idiom_name = "Phone"
        elif interface_idiom_value == 1:
            interface_idiom_name = "Pad"
        return interface_idiom_name

    def get_interface_idiom_summary(self):
        interface_idiom_name = self.get_interface_idiom_value()
        if interface_idiom_name is None:
            return None
        return "idiom={}".format(interface_idiom_name)

    def summary(self):
        bounds_summary = self.get_bounds_summary()
        scale_summary = self.get_scale_summary()
        # horizontal_scale_summary = self.get_horizontal_scale_summary()
        interface_idiom_summary = self.get_interface_idiom_summary()

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
