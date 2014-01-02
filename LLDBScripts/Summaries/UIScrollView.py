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
import UIView


class UIScrollView_SynthProvider(UIView.UIView_SynthProvider):
    # UIScrollView:
    # Offset / size (+ alignment)                                           32bit:                  64bit:
    #
    # id _delegate                                                           96 = 0x60 / 4          184 = 0xb8 / 8
    # CGSize _contentSize                                                   100 = 0x64 / 8          192 = 0xc0 / 16
    # UIEdgeInsets _contentInset                                            108 = 0x6c / 16         208 = 0xd0 / 32
    # UIImageView *_verticalScrollIndicator                                 124 = 0x7c / 4          240 = 0xf0 / 8
    # UIImageView *_horizontalScrollIndicator                               128 = 0x80 / 4          248 = 0xf8 / 8
    # _UIStaticScrollBar *_staticScrollBar                                  132 = 0x84 / 4          256 = 0x100 / 8
    # UIEdgeInsets _scrollIndicatorInset                                    136 = 0x88 / 16         264 = 0x108 / 32
    # double _startOffsetX                                                  152 = 0x98 / 8          296 = 0x128 / 8
    # double _startOffsetY                                                  160 = 0xa0 / 8          304 = 0x130 / 8
    # double _lastUpdateOffsetX                                             168 = 0xa8 / 8          312 = 0x138 / 8
    # double _lastUpdateOffsetY                                             176 = 0xb0 / 8          320 = 0x140 / 8
    # double _lastUpdateTime                                                184 = 0xb8 / 8          328 = 0x148 / 8
    # CGFloat _minimumZoomScale                                             192 = 0xc0 / 4          336 = 0x150 / 8
    # CGFloat _maximumZoomScale                                             196 = 0xc4 / 4          344 = 0x158 / 8
    # UIView *_zoomView                                                     200 = 0xc8 / 4          352 = 0x160 / 8
    # double _horizontalVelocity                                            204 = 0xcc / 8          360 = 0x168 / 8
    # double _verticalVelocity                                              212 = 0xd4 / 8          368 = 0x170 / 8
    # double _previousHorizontalVelocity                                    220 = 0xdc / 8          376 = 0x178 / 8
    # double _previousVerticalVelocity                                      228 = 0xe4 / 8          384 = 0x180 / 8
    # id _scrollHeartbeat                                                   236 = 0xec / 4          392 = 0x188 / 8
    # CGPoint _pageDecelerationTarget                                       240 = 0xf0 / 8          400 = 0x190 / 16
    # CGSize _decelerationFactor                                            248 = 0xf8 / 8          416 = 0x1a0 / 16
    # CGPoint _adjustedDecelerationTarget                                   256 = 0x100 / 8         432 = 0x1b0 / 16
    # CGSize _adjustedDecelerationFactor                                    264 = 0x108 / 8         448 = 0x1c0 / 16
    # double _decelerationLnFactorH                                         272 = 0x110 / 8         464 = 0x1d0 / 8
    # double _decelerationLnFactorV                                         280 = 0x118 / 8         472 = 0x1d8 / 8
    # id *_shadows                                                          288 = 0x120 / 4         480 = 0x1e0 / 8
    # id _scrollNotificationViews                                           292 = 0x124 / 4         488 = 0x1e8 / 8
    # double _contentOffsetAnimationDuration                                296 = 0x128 / 8         496 = 0x1f0 / 8
    # id _animation                                                         304 = 0x130 / 4         504 = 0x1f8 / 8
    # id _zoomAnimation                                                     308 = 0x134 / 4         512 = 0x200 / 8
    # id _pinch                                                             312 = 0x138 / 4         520 = 0x208 / 8
    # id _pan                                                               316 = 0x13c / 4         528 = 0x210 / 8
    # id _swipe                                                             320 = 0x140 / 4         536 = 0x218 / 8
    # id _touchDelayGestureRecognizer                                       324 = 0x144 / 4         544 = 0x220 / 8
    # UISwipeGestureRecognizer *_lowFidelitySwipeGestureRecognizers[4]      328 = 0x148 / 16        552 = 0x228 / 32
    # UIScrollView *_draggingChildScrollView                                344 = 0x158 / 4         584 = 0x248 / 8
    # CGPoint _parentAdjustment                                             348 = 0x15c / 8         592 = 0x250 / 16
    # CGFloat _pagingSpringPull                                             356 = 0x164 / 4         608 = 0x260 / 8
    # CGFloat _pagingFriction                                               360 = 0x168 / 4         616 = 0x268 / 8
    # NSInteger _fastScrollCount                                            364 = 0x16c / 4         624 = 0x270 / 8
    # CGFloat _fastScrollMultiplier                                         368 = 0x170 / 4         632 = 0x278 / 8
    # CGFloat _fastScrollStartMultiplier                                    372 = 0x174 / 4         640 = 0x280 / 8
    # double _fastScrollEndTime                                             376 = 0x178 / 8         648 = 0x288 / 8
    # CGPoint _rotationCenterPoint                                          384 = 0x180 / 8         656 = 0x290 / 16
    # CGFloat _accuracy                                                     388 = 0x188 / 4         672 = 0x2a0 / 8
    # NSUInteger _zoomAnimationCount                                        396 = 0x18c / 4         680 = 0x2a8 / 8
    # CGSize _accumulatedOffset                                             400 = 0x190 / 8         688 = 0x2b0 / 16
    # NSInteger _touchLevel                                                 408 = 0x198 / 4         704 = 0x2c0 / 8
    # CGFloat _savedKeyboardAdjustmentDelta                                 412 = 0x19c / 4         712 = 0x2c8 / 8
    # struct {
    #     unsigned tracking : 1
    #     unsigned dragging : 1
    #     unsigned verticalBounceEnabled : 1
    #     unsigned horizontalBounceEnabled : 1
    #     unsigned verticalBouncing : 1
    #     unsigned horizontalBouncing : 1
    #     unsigned bouncesZoom : 1
    #     unsigned zoomBouncing : 1
    #     unsigned alwaysBounceHorizontal : 1
    #     unsigned alwaysBounceVertical : 1
    #     unsigned preventScrollingContainer : 1
    #     unsigned canCancelContentTouches : 1
    #     unsigned delaysContentTouches : 1
    #     unsigned programmaticScrollDisabled : 1
    #     unsigned scrollDisabled : 1
    #     unsigned zoomDisabled : 1
    #     unsigned scrollTriggered : 1
    #     unsigned showsHorizontalScrollIndicator : 1
    #     unsigned showsVerticalScrollIndicator : 1
    #     unsigned indicatorStyle : 2
    #     unsigned inZoom : 1
    #     unsigned hideIndicatorsInZoom : 1
    #     unsigned pushedTrackingMode : 1
    #     unsigned displayingScrollIndicators : 1
    #     unsigned verticalIndicatorShrunk : 1
    #     unsigned horizontalIndicatorShrunk : 1
    #     unsigned contentFitDisableScrolling : 1
    #     unsigned pagingEnabled : 1
    #     unsigned pagingLeft : 1
    #     unsigned pagingRight : 1
    #     unsigned pagingUp : 1
    #     unsigned pagingDown : 1
    #     unsigned lastHorizontalDirection : 1
    #     unsigned lastVerticalDirection : 1
    #     unsigned dontScrollToTop : 1
    #     unsigned scrollingToTop : 1
    #     unsigned singleFingerPan : 1
    #     unsigned autoscrolling : 1
    #     unsigned automaticContentOffsetAdjustmentDisabled : 1
    #     unsigned skipStartOffsetAdjustment : 1
    #     unsigned delegateScrollViewDidScroll : 1
    #     unsigned delegateScrollViewDidZoom : 1
    #     unsigned delegateContentSizeForZoomScale : 1
    #     unsigned preserveCenterDuringRotation : 1
    #     unsigned delaysTrackingWhileDecelerating : 1
    #     unsigned pinnedZoomMin : 1
    #     unsigned pinnedXMin : 1
    #     unsigned pinnedYMin : 1
    #     unsigned pinnedXMax : 1
    #     unsigned pinnedYMax : 1
    #     unsigned skipLinkChecks : 1
    #     unsigned staysCenteredDuringPinch : 1
    #     unsigned wasDelayingPinchForSystemGestures : 1
    #     unsigned systemGesturesRecognitionPossible : 1
    #     unsigned disableContentOffsetRounding : 1
    #     unsigned adjustedDecelerationTargetX : 1
    #     unsigned adjustedDecelerationTargetY : 1
    #     unsigned hasScrolled : 1
    #     unsigned wantsConstrainedContentSize : 1
    #     unsigned updateInsetBottom : 1
    #     unsigned beingDraggedByChildScrollView : 1
    #     unsigned adjustsTargetsOnContentOffsetChanges : 1
    # } _scrollViewFlags                                                    416 = 0x1a0 / 8         720 = 0x2d0 / 8
    # BOOL _useContentDimensionVariablesForConstraintLowering               424 = 0x1a8 / 1 + 3     728 = 0x2d8 / 1 + 7
    # id _scrollTestParameters                                              428 = 0x1ac / 4         736 = 0x2e0 / 8
    # NSInteger _keyboardDismissMode                                        432 = 0x1b0 / 4         744 = 0x2e8 / 8
    # NSISVariable *_contentWidthVariable                                   436 = 0x1b4 / 4         752 = 0x2f0 / 8
    # NSISVariable *_contentHeightVariable                                  440 = 0x1b8 / 4         760 = 0x2f8 / 8
    # NSArray *_automaticContentConstraints                                 444 = 0x1bc / 4         768 = 0x300 / 8
    # CADoublePoint _zoomAnchorPoint                                        448 = 0x1c0 / 16        776 = 0x308 / 16

    def __init__(self, value_obj, sys_params, internal_dict):
        # self.as_super = super(UIScrollView_SynthProvider, self)
        # self.as_super.__init__(value_obj, sys_params, internal_dict)
        super(UIScrollView_SynthProvider, self).__init__(value_obj, sys_params, internal_dict)

        self.content_size = None
        self.content_inset = None
        self.minimum_zoom_scale = None
        self.maximum_zoom_scale = None

        self.update()

    def update(self):
        self.content_size = None
        self.content_inset = None
        self.minimum_zoom_scale = None
        self.maximum_zoom_scale = None
        super(UIScrollView_SynthProvider, self).update()

    def adjust_for_architecture(self):
        super(UIScrollView_SynthProvider, self).adjust_for_architecture()

    def get_content_size(self):
        if self.content_size:
            return self.content_size

        if self.sys_params.is_64_bit:
            offset = 0xc0
        else:
            offset = 0x64

        self.content_size = self.value_obj.CreateChildAtOffset("contentSize",
                                                               offset,
                                                               self.sys_params.types_cache.CGSize)
        return self.content_size

    def get_content_inset(self):
        if self.content_inset:
            return self.content_inset

        if self.sys_params.is_64_bit:
            offset = 0xd0
        else:
            offset = 0x6c

        self.content_inset = self.value_obj.CreateChildAtOffset("contentInset",
                                                                offset,
                                                                self.sys_params.types_cache.UIEdgeInsets)
        return self.content_inset

    def get_minimum_zoom_scale(self):
        if self.minimum_zoom_scale:
            return self.minimum_zoom_scale

        if self.sys_params.is_64_bit:
            offset = 0x150
        else:
            offset = 0xc0

        self.minimum_zoom_scale = self.value_obj.CreateChildAtOffset("minimumZoomScale",
                                                                     offset,
                                                                     self.sys_params.types_cache.CGFloat)
        return self.minimum_zoom_scale

    def get_maximum_zoom_scale(self):
        if self.maximum_zoom_scale:
            return self.maximum_zoom_scale

        if self.sys_params.is_64_bit:
            offset = 0x158
        else:
            offset = 0xc4

        self.maximum_zoom_scale = self.value_obj.CreateChildAtOffset("maximumZoomScale",
                                                                     offset,
                                                                     self.sys_params.types_cache.CGFloat)
        return self.maximum_zoom_scale

    def summary(self):
        content_size = self.get_content_size()
        content_size_w = float(content_size.GetChildMemberWithName("width").GetValue())
        content_size_h = float(content_size.GetChildMemberWithName("height").GetValue())
        content_size_summary = "contentSize=({:.0f}, {:.0f})".format(content_size_w, content_size_h)

        content_inset = self.get_content_inset()
        content_inset_t = float(content_inset.GetChildMemberWithName("top").GetValue())
        content_inset_l = float(content_inset.GetChildMemberWithName("left").GetValue())
        content_inset_b = float(content_inset.GetChildMemberWithName("bottom").GetValue())
        content_inset_r = float(content_inset.GetChildMemberWithName("right").GetValue())
        content_inset_summary = "inset=({:.0f}, {:.0f}, {:.0f}, {:.0f})".\
            format(content_inset_t, content_inset_l, content_inset_b, content_inset_r)

        minimum_zoom_scale = self.get_minimum_zoom_scale()
        minimum_zoom_scale_value = float(minimum_zoom_scale.GetValue())
        minimum_zoom_scale_summary = "minScale={:.2f}".format(minimum_zoom_scale_value)

        maximum_zoom_scale = self.get_maximum_zoom_scale()
        maximum_zoom_scale_value = float(maximum_zoom_scale.GetValue())
        maximum_zoom_scale_summary = "maxScale={:.2f}".format(maximum_zoom_scale_value)

        # Summaries
        summaries = [content_size_summary]
        if content_inset_t != 0 or content_inset_l != 0 or content_inset_b != 0 or content_inset_r != 0:
            summaries.append(content_inset_summary)
        if minimum_zoom_scale_value != 1:
            summaries.append(minimum_zoom_scale_summary)
        if maximum_zoom_scale_value != 1:
            summaries.append(maximum_zoom_scale_summary)
        summary = ", ".join(summaries)
        return summary


def UIScrollView_SummaryProvider(value_obj, internal_dict):
    return summary_helpers.generic_SummaryProvider(value_obj, internal_dict, UIScrollView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIScrollView.UIScrollView_SummaryProvider \
                            --category UIKit \
                            UIScrollView")
    debugger.HandleCommand("type category enable UIKit")
