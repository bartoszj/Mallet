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
import objc_runtime
import summary_helpers

statistics = lldb.formatters.metrics.Metrics()
statistics.add_metric('invalid_isa')
statistics.add_metric('invalid_pointer')
statistics.add_metric('unknown_class')
statistics.add_metric('code_notrun')


class UIView_SynthProvider(object):
    # UIView:
    # Offset / size                                 32bit:              64bit:
    #
    # Class isa                                      0 = 0x00 / 4        0 = 0x00 / 8
    # CALayer *_layer                                4 = 0x04 / 4        8 = 0x08 / 8
    # id _gestureInfo                                8 = 0x08 / 4       16 = 0x10 / 8
    # NSMutableArray *_gestureRecognizers           12 = 0x0c / 4       24 = 0x18 / 8
    # NSArray *_subviewCache                        16 = 0x10 / 4       32 = 0x20 / 8
    # float _charge                                 20 = 0x14 / 4       40 = 0x28 / 8
    # int _tag                                      24 = 0x18 / 4       48 = 0x30 / 4 + 4
    # UIViewController *_viewDelegate               28 = 0x1c / 4       56 = 0x38 / 8
    # NSString *_backgroundColorSystemColorName     32 = 0x20 / 4       64 = 0x40 / 8
    # unsigned _countOfMotionEffectsInSubtree       36 = 0x24 / 4       72 = 0x48 / 4 + 4
    # struct {
    #     unsigned userInteractionDisabled : 1
    #     unsigned implementsDrawRect : 1
    #     unsigned implementsDidScroll : 1
    #     unsigned implementsMouseTracking : 1
    #     unsigned hasBackgroundColor : 1
    #     unsigned isOpaque : 1
    #     unsigned becomeFirstResponderWhenCapable : 1
    #     unsigned interceptMouseEvent : 1
    #     unsigned deallocating : 1
    #     unsigned debugFlash : 1
    #     unsigned debugSkippedSetNeedsDisplay : 1
    #     unsigned debugScheduledDisplayIsRequired : 1
    #     unsigned isInAWindow : 1
    #     unsigned isAncestorOfFirstResponder : 1
    #     unsigned dontAutoresizeSubviews : 1
    #     unsigned autoresizeMask : 6
    #     unsigned patternBackground : 1
    #     unsigned fixedBackgroundPattern : 1
    #     unsigned dontAnimate : 1
    #     unsigned superLayerIsView : 1
    #     unsigned layerKitPatternDrawing : 1
    #     unsigned multipleTouchEnabled : 1
    #     unsigned exclusiveTouch : 1
    #     unsigned hasViewController : 1
    #     unsigned needsDidAppearOrDisappear : 1
    #     unsigned gesturesEnabled : 1
    #     unsigned deliversTouchesForGesturesToSuperview : 1
    #     unsigned chargeEnabled : 1
    #     unsigned skipsSubviewEnumeration : 1
    #     unsigned needsDisplayOnBoundsChange : 1
    #     unsigned hasTiledLayer : 1
    #     unsigned hasLargeContent : 1
    #     unsigned unused : 1
    #     unsigned traversalMark : 1
    #     unsigned appearanceIsInvalid : 1
    #     unsigned monitorsSubtree : 1
    #     unsigned hostsAutolayoutEngine : 1
    #     unsigned constraintsAreClean : 1
    #     unsigned subviewLayoutConstraintsAreClean : 1
    #     unsigned intrinsicContentSizeConstraintsAreClean : 1
    #     unsigned potentiallyHasDanglyConstraints : 1
    #     unsigned doesNotTranslateAutoresizingMaskIntoConstraints : 1
    #     unsigned autolayoutIsClean : 1
    #     unsigned subviewsAutolayoutIsClean : 1
    #     unsigned layoutFlushingDisabled : 1
    #     unsigned layingOutFromConstraints : 1
    #     unsigned wantsAutolayout : 1
    #     unsigned subviewWantsAutolayout : 1
    #     unsigned isApplyingValuesFromEngine : 1
    #     unsigned isInAutolayout : 1
    #     unsigned isUpdatingAutoresizingConstraints : 1
    #     unsigned isUpdatingConstraints : 1
    #     unsigned stayHiddenAwaitingReuse : 1
    #     unsigned stayHiddenAfterReuse : 1
    #     unsigned skippedLayoutWhileHiddenForReuse : 1
    #     unsigned hasMaskView : 1
    #     unsigned hasVisualAltitude : 1
    #     unsigned hasBackdropMaskViews : 1
    #     unsigned backdropMaskViewFlags : 3
    #     unsigned delaysTouchesForSystemGestures : 1
    #     unsigned subclassShouldDelayTouchForSystemGestures : 1
    #     unsigned hasMotionEffects : 1
    #     unsigned backdropOverlayMode : 2
    #     unsigned tintAdjustmentMode : 2
    #     unsigned isReferenceView : 1
    # } _viewFlags                                  40 = 0x28 / 10 + 2  80 = 0x50 / 10 + 6
    # int _retainCount                              52 = 0x34 / 4       96 = 0x60 / 8?
    # int _tintAdjustmentDimmingCount               56 = 0x38 / 4      100 = 0x64 / 8?
    # BOOL _shouldArchiveUIAppearanceTags           60 = 0x3c / 1 + 3  104 = 0x68 / 1 + 7
    # UIColor *_interactionTintColor                64 = 0x40 / 4      120 = 0x78 / 8
    # NSISEngine *_layoutEngine                     68 = 0x44 / 4      128 = 0x80 / 8
    # NSISVariable *_boundsWidthVariable            72 = 0x48 / 4      136 = 0x88 / 8
    # NSISVariable *_boundsHeightVariable           76 = 0x4c / 4      144 = 0x90 / 8
    # NSISVariable *_minXVariable                   80 = 0x50 / 4      152 = 0x98 / 8
    # NSISVariable *_minYVariable                   84 = 0x54 / 4      160 = 0xa0 / 8
    # NSMutableArray *_internalConstraints          88 = 0x58 / 4      168 = 0xa8 / 8
    # NSArray *_constraintsExceptingSubviewAutoresizingConstraints  92 = 0x5c / 4       176 = 0xb0 / 8

    def __init__(self, value_obj, sys_params, internal_dict):
        # self.as_super = super(UIView_SynthProvider, self)
        # self.as_super.__init__()
        super(UIView_SynthProvider, self).__init__()
        self.value_obj = value_obj
        self.sys_params = sys_params
        self.internal_dict = internal_dict

        self.stream = lldb.SBStream()
        self.value_obj.GetExpressionPath(self.stream)

        self.update()

    def update(self):
        self.adjust_for_architecture()

    def adjust_for_architecture(self):
        pass

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

    def summary(self):
        # Frame
        frame = self.get_frame()
        # Origin
        origin = frame.GetChildMemberWithName("origin")
        x = float(origin.GetChildMemberWithName("x").GetValue())
        y = float(origin.GetChildMemberWithName("y").GetValue())
        # Size
        size = frame.GetChildMemberWithName("size")
        w = float(size.GetChildMemberWithName("width").GetValue())
        h = float(size.GetChildMemberWithName("height").GetValue())

        frame_summary = "frame=({:.4}, {:.4}; {:.4}, {:.4})".format(x, y, w, h)

        # Alpha
        alpha = float(self.get_alpha().GetValue())
        alpha_summary = "alpha={:4.2}".format(alpha)

        # Hidden
        hidden = self.get_hidden().GetValueAsUnsigned()
        hidden_summary = "hidden={}".format("YES" if hidden == 1 else "NO")

        summaries = [frame_summary]
        if alpha != 1.0:
            summaries.append(alpha_summary)
        if hidden != 0:
            summaries.append(hidden_summary)

        summary = ", ".join(summaries)
        return summary


def UIView_SummaryProvider(value_obj, internal_dict):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    supported_classes = ["UIView", "UIWindow"]
    if not class_data.is_valid() or class_data.class_name() not in supported_classes:
        return ""
    summary_helpers.update_sys_params(value_obj, class_data.sys_params)
    if wrapper is not None:
        return wrapper.message()

    wrapper = UIView_SynthProvider(value_obj, class_data.sys_params, internal_dict)
    if wrapper is not None:
        return wrapper.summary()
    return "Summary Unavailable"


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIView.UIView_SummaryProvider \
                            --category UIKit \
                            UIView UIWindow")
    debugger.HandleCommand("type category enable UIKit")
