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
import UIResponder


class UIView_SynthProvider(UIResponder.UIResponder_SynthProvider):
    # Class: UIView
    # Super class: UIResponder
    # Protocols: _UIScrollNotification, UITextEffectsOrdering, NSISVariableDelegate, NSLayoutItem, NSISEngineDelegate, NSCoding, UIAppearance, UIAppearanceContainer, UIDynamicItem
    # Name:                                                                       armv7                 i386                  arm64                 x86_64
    # CALayer * _layer                                                         44 (0x02C) / 4        44 (0x02C) / 4        88 (0x058) / 8        88 (0x058) / 8
    # id _gestureInfo                                                          48 (0x030) / 4        48 (0x030) / 4        96 (0x060) / 8        96 (0x060) / 8
    # NSMutableArray * _gestureRecognizers                                     52 (0x034) / 4        52 (0x034) / 4       104 (0x068) / 8       104 (0x068) / 8
    # NSArray * _subviewCache                                                  56 (0x038) / 4        56 (0x038) / 4       112 (0x070) / 8       112 (0x070) / 8
    # float _charge                                                            60 (0x03C) / 4        60 (0x03C) / 4       120 (0x078) / 4  + 4  120 (0x078) / 4  + 4
    # NSInteger _tag                                                           64 (0x040) / 4        64 (0x040) / 4       128 (0x080) / 8       128 (0x080) / 8
    # UIViewController * _viewDelegate                                         68 (0x044) / 4        68 (0x044) / 4       136 (0x088) / 8       136 (0x088) / 8
    # NSString * _backgroundColorSystemColorName                               72 (0x048) / 4        72 (0x048) / 4       144 (0x090) / 8       144 (0x090) / 8
    # NSUInteger _countOfMotionEffectsInSubtree                                76 (0x04C) / 4        76 (0x04C) / 4       152 (0x098) / 8       152 (0x098) / 8
    # struct {
    #         unsigned int userInteractionDisabled:1;
    #         unsigned int implementsDrawRect:1;
    #         unsigned int implementsDidScroll:1;
    #         unsigned int implementsMouseTracking:1;
    #         unsigned int hasBackgroundColor:1;
    #         unsigned int isOpaque:1;
    #         unsigned int becomeFirstResponderWhenCapable:1;
    #         unsigned int interceptMouseEvent:1;
    #         unsigned int deallocating:1;
    #         unsigned int debugFlash:1;
    #         unsigned int debugSkippedSetNeedsDisplay:1;
    #         unsigned int debugScheduledDisplayIsRequired:1;
    #         unsigned int isInAWindow:1;
    #         unsigned int isAncestorOfFirstResponder:1;
    #         unsigned int dontAutoresizeSubviews:1;
    #         unsigned int autoresizeMask:6;
    #         unsigned int patternBackground:1;
    #         unsigned int fixedBackgroundPattern:1;
    #         unsigned int dontAnimate:1;
    #         unsigned int superLayerIsView:1;
    #         unsigned int layerKitPatternDrawing:1;
    #         unsigned int multipleTouchEnabled:1;
    #         unsigned int exclusiveTouch:1;
    #         unsigned int hasViewController:1;
    #         unsigned int needsDidAppearOrDisappear:1;
    #         unsigned int gesturesEnabled:1;
    #         unsigned int deliversTouchesForGesturesToSuperview:1;
    #         unsigned int chargeEnabled:1;
    #         unsigned int skipsSubviewEnumeration:1;
    #         unsigned int needsDisplayOnBoundsChange:1;
    #         unsigned int hasTiledLayer:1;
    #         unsigned int hasLargeContent:1;
    #         unsigned int unused:1;
    #         unsigned int traversalMark:1;
    #         unsigned int appearanceIsInvalid:1;
    #         unsigned int monitorsSubtree:1;
    #         unsigned int hostsAutolayoutEngine:1;
    #         unsigned int constraintsAreClean:1;
    #         unsigned int subviewLayoutConstraintsAreClean:1;
    #         unsigned int intrinsicContentSizeConstraintsAreClean:1;
    #         unsigned int potentiallyHasDanglyConstraints:1;
    #         unsigned int doesNotTranslateAutoresizingMaskIntoConstraints:1;
    #         unsigned int autolayoutIsClean:1;
    #         unsigned int subviewsAutolayoutIsClean:1;
    #         unsigned int layoutFlushingDisabled:1;
    #         unsigned int layingOutFromConstraints:1;
    #         unsigned int wantsAutolayout:1;
    #         unsigned int subviewWantsAutolayout:1;
    #         unsigned int isApplyingValuesFromEngine:1;
    #         unsigned int isInAutolayout:1;
    #         unsigned int isUpdatingAutoresizingConstraints:1;
    #         unsigned int isUpdatingConstraints:1;
    #         unsigned int stayHiddenAwaitingReuse:1;
    #         unsigned int stayHiddenAfterReuse:1;
    #         unsigned int skippedLayoutWhileHiddenForReuse:1;
    #         unsigned int hasMaskView:1;
    #         unsigned int hasVisualAltitude:1;
    #         unsigned int hasBackdropMaskViews:1;
    #         unsigned int backdropMaskViewFlags:3;
    #         unsigned int delaysTouchesForSystemGestures:1;
    #         unsigned int subclassShouldDelayTouchForSystemGestures:1;
    #         unsigned int hasMotionEffects:1;
    #         unsigned int backdropOverlayMode:2;
    #         unsigned int tintAdjustmentMode:2;
    #         unsigned int isReferenceView:1;
    #         unsigned int focusState:2;
    #         unsigned int hasUserInterfaceIdiom:1;
    #         unsigned int userInterfaceIdiom:3;
    #         unsigned int ancestorDefinesTintColor:1;
    #         unsigned int ancestorDefinesTintAdjustmentMode:1;
    #     } _viewFlags                                                         80 (0x050) / 11 + 1   80 (0x050) / 12      160 (0x0A0) / 12 + 4  160 (0x0A0) / 12 + 4
    # NSInteger _retainCount                                                   92 (0x05C) / 4        92 (0x05C) / 4       176 (0x0B0) / 8       176 (0x0B0) / 8
    # NSInteger _tintAdjustmentDimmingCount                                    96 (0x060) / 4        96 (0x060) / 4       184 (0x0B8) / 8       184 (0x0B8) / 8
    # BOOL _shouldArchiveUIAppearanceTags                                     100 (0x064) / 1  + 3  100 (0x064) / 1  + 3  192 (0x0C0) / 1  + 7  192 (0x0C0) / 1  + 7
    # UIColor * _interactionTintColor                                         104 (0x068) / 4       104 (0x068) / 4       200 (0x0C8) / 8       200 (0x0C8) / 8
    # NSISEngine * _layoutEngine                                              108 (0x06C) / 4       108 (0x06C) / 4       208 (0x0D0) / 8       208 (0x0D0) / 8
    # NSISVariable * _boundsWidthVariable                                     112 (0x070) / 4       112 (0x070) / 4       216 (0x0D8) / 8       216 (0x0D8) / 8
    # NSISVariable * _boundsHeightVariable                                    116 (0x074) / 4       116 (0x074) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # NSISVariable * _minXVariable                                            120 (0x078) / 4       120 (0x078) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # NSISVariable * _minYVariable                                            124 (0x07C) / 4       124 (0x07C) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # NSMutableArray * _internalConstraints                                   128 (0x080) / 4       128 (0x080) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # NSArray * _constraintsExceptingSubviewAutoresizingConstraints           132 (0x084) / 4       132 (0x084) / 4       256 (0x100) / 8       256 (0x100) / 8

    def __init__(self, value_obj, internal_dict):
        super(UIView_SynthProvider, self).__init__(value_obj, internal_dict)

        self.stream = lldb.SBStream()
        self.value_obj.GetExpressionPath(self.stream)

    def get_origin(self):
        origin = self.value_obj.CreateValueFromExpression("frameOrigin",
                                                          "(CGPoint)[{} frameOrigin]"
                                                          .format(self.stream.GetData()))
        return origin

    def get_size(self):
        size = self.value_obj.CreateValueFromExpression("size",
                                                        "(CGSize)[{} size]"
                                                        .format(self.stream.GetData()))
        return size

    def get_frame(self):
        frame = self.value_obj.CreateValueFromExpression("frame",
                                                         "(CGRect)[{} frame]"
                                                         .format(self.stream.GetData()))
        return frame

    def get_alpha(self):
        alpha = self.value_obj.CreateValueFromExpression("alpha",
                                                         "(CGFloat)[{} alpha]"
                                                         .format(self.stream.GetData()))
        return alpha

    def get_hidden(self):
        hidden = self.value_obj.CreateValueFromExpression("hidden",
                                                          "(BOOL)[{} isHidden]"
                                                          .format(self.stream.GetData()))
        return hidden

    # def summary(self):
    #     # Frame
    #     frame = self.get_frame()
    #     # Origin
    #     origin = frame.GetChildMemberWithName("origin")
    #     x = float(origin.GetChildMemberWithName("x").GetValue())
    #     y = float(origin.GetChildMemberWithName("y").GetValue())
    #     # Size
    #     size = frame.GetChildMemberWithName("size")
    #     w = float(size.GetChildMemberWithName("width").GetValue())
    #     h = float(size.GetChildMemberWithName("height").GetValue())
    #
    #     frame_summary = "frame=({:.0f}, {:.0f}; {:.0f}, {:.0f})".format(x, y, w, h)
    #
    #     # Alpha
    #     alpha = float(self.get_alpha().GetValue())
    #     alpha_summary = "alpha={:4.2}".format(alpha)
    #
    #     # Hidden
    #     hidden = self.get_hidden().GetValueAsUnsigned()
    #     hidden_summary = "hidden={}".format("YES" if hidden == 1 else "NO")
    #
    #     summaries = [frame_summary]
    #     if alpha != 1.0:
    #         summaries.append(alpha_summary)
    #     if hidden != 0:
    #         summaries.append(hidden_summary)
    #
    #     summary = ", ".join(summaries)
    #     return summary


def UIView_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIView_SynthProvider,
                                            ["UIImageView", "UIView", "UIWindow"])


# def __lldb_init_module(debugger, dict):
    # debugger.HandleCommand("type summary add -F UIView.UIView_SummaryProvider \
    #                         --category UIKit \
    #                         UIImageView UIView UIWindow")
    # debugger.HandleCommand("type category enable UIKit")
