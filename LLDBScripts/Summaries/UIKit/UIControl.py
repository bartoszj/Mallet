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

import UIView


class UIControl_SynthProvider(UIView.UIView_SynthProvider):
    # Class: UIControl
    # Super class: UIView
    # Name:                                                  armv7                 i386                  arm64                 x86_64
    # NSMutableArray * _targetActions                     96 (0x060) / 4        96 (0x060) / 4       184 (0x0B8) / 8       184 (0x0B8) / 8
    # CGPoint _previousPoint                             100 (0x064) / 8       100 (0x064) / 8       192 (0x0C0) / 16      192 (0x0C0) / 16
    # double _downTime                                   108 (0x06C) / 8       108 (0x06C) / 8       208 (0x0D0) / 8       208 (0x0D0) / 8
    # struct {
    #         unsigned int disabled:1;
    #         unsigned int tracking:1;
    #         unsigned int touchInside:1;
    #         unsigned int touchDragged:1;
    #         unsigned int requiresDisplayOnTracking:1;
    #         unsigned int highlighted:1;
    #         unsigned int dontHighlightOnTouchDown:1;
    #         unsigned int delayActions:1;
    #         unsigned int allowActionsToQueue:1;
    #         unsigned int pendingUnhighlight:1;
    #         unsigned int selected:1;
    #         unsigned int verticalAlignment:2;
    #         unsigned int horizontalAlignment:2;
    #         unsigned int wasLastHighlightSuccessful:1;
    #         unsigned int touchHasHighlighted:1;
    #     } _controlFlags                                116 (0x074) / 3       116 (0x074) / 4       216 (0x0D8) / 4       216 (0x0D8) / 4

    def __init__(self, value_obj, internal_dict):
        super(UIControl_SynthProvider, self).__init__(value_obj, internal_dict)
