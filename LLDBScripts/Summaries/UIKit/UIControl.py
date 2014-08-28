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
    # UIControl:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # NSMutableArray *_targetActions                                         96 = 0x60 / 4          184 = 0xb8 / 8
    # CGPoint _previousPoint                                                100 = 0x64 / 8          192 = 0xc0 / 16
    # double _downTime                                                      108 = 0x6c / 8          208 = 0xd0 / 8
    # struct {
    #     unsigned disabled : 1;
    #     unsigned tracking : 1;
    #     unsigned touchInside : 1;
    #     unsigned touchDragged : 1;
    #     unsigned requiresDisplayOnTracking : 1;
    #     unsigned highlighted : 1;
    #     unsigned dontHighlightOnTouchDown : 1;
    #     unsigned delayActions : 1;
    #     unsigned allowActionsToQueue : 1;
    #     unsigned pendingUnhighlight : 1;
    #     unsigned selected : 1;
    #     unsigned verticalAlignment : 2;
    #     unsigned horizontalAlignment : 2;
    #     unsigned wasLastHighlightSuccessful : 1;
    #     unsigned touchHasHighlighted : 1;
    # } _controlFlags                                                       116 = 0x74 / 3 + 1      216 = 0xd8 / 3 + 1

    def __init__(self, value_obj, internal_dict):
        super(UIControl_SynthProvider, self).__init__(value_obj, internal_dict)
