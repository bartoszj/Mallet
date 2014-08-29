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
import UIView
import CGSize


class UIScrollView_SynthProvider(UIView.UIView_SynthProvider):
    # Class: UIScrollView
    # Super class: UIView
    # Protocols: _UIScrollToTopView, NSCoding
    # Name:                                                                 armv7                 i386                  arm64                 x86_64
    # id _delegate                                                       96 (0x060) / 4        96 (0x060) / 4       184 (0x0B8) / 8       184 (0x0B8) / 8
    # CGSize _contentSize                                               100 (0x064) / 8       100 (0x064) / 8       192 (0x0C0) / 16      192 (0x0C0) / 16
    # UIEdgeInsets _contentInset                                        108 (0x06C) / 16      108 (0x06C) / 16      208 (0x0D0) / 32      208 (0x0D0) / 32
    # UIImageView * _verticalScrollIndicator                            124 (0x07C) / 4       124 (0x07C) / 4       240 (0x0F0) / 8       240 (0x0F0) / 8
    # UIImageView * _horizontalScrollIndicator                          128 (0x080) / 4       128 (0x080) / 4       248 (0x0F8) / 8       248 (0x0F8) / 8
    # _UIStaticScrollBar * _staticScrollBar                             132 (0x084) / 4       132 (0x084) / 4       256 (0x100) / 8       256 (0x100) / 8
    # UIEdgeInsets _scrollIndicatorInset                                136 (0x088) / 16      136 (0x088) / 16      264 (0x108) / 32      264 (0x108) / 32
    # double _startOffsetX                                              152 (0x098) / 8       152 (0x098) / 8       296 (0x128) / 8       296 (0x128) / 8
    # double _startOffsetY                                              160 (0x0A0) / 8       160 (0x0A0) / 8       304 (0x130) / 8       304 (0x130) / 8
    # double _lastUpdateOffsetX                                         168 (0x0A8) / 8       168 (0x0A8) / 8       312 (0x138) / 8       312 (0x138) / 8
    # double _lastUpdateOffsetY                                         176 (0x0B0) / 8       176 (0x0B0) / 8       320 (0x140) / 8       320 (0x140) / 8
    # double _lastUpdateTime                                            184 (0x0B8) / 8       184 (0x0B8) / 8       328 (0x148) / 8       328 (0x148) / 8
    # CGFloat _minimumZoomScale                                         192 (0x0C0) / 4       192 (0x0C0) / 4       336 (0x150) / 8       336 (0x150) / 8
    # CGFloat _maximumZoomScale                                         196 (0x0C4) / 4       196 (0x0C4) / 4       344 (0x158) / 8       344 (0x158) / 8
    # UIView * _zoomView                                                200 (0x0C8) / 4       200 (0x0C8) / 4       352 (0x160) / 8       352 (0x160) / 8
    # double _horizontalVelocity                                        204 (0x0CC) / 8       204 (0x0CC) / 8       360 (0x168) / 8       360 (0x168) / 8
    # double _verticalVelocity                                          212 (0x0D4) / 8       212 (0x0D4) / 8       368 (0x170) / 8       368 (0x170) / 8
    # double _previousHorizontalVelocity                                220 (0x0DC) / 8       220 (0x0DC) / 8       376 (0x178) / 8       376 (0x178) / 8
    # double _previousVerticalVelocity                                  228 (0x0E4) / 8       228 (0x0E4) / 8       384 (0x180) / 8       384 (0x180) / 8
    # id _scrollHeartbeat                                               236 (0x0EC) / 4       236 (0x0EC) / 4       392 (0x188) / 8       392 (0x188) / 8
    # CGPoint _pageDecelerationTarget                                   240 (0x0F0) / 8       240 (0x0F0) / 8       400 (0x190) / 16      400 (0x190) / 16
    # CGSize _decelerationFactor                                        248 (0x0F8) / 8       248 (0x0F8) / 8       416 (0x1A0) / 16      416 (0x1A0) / 16
    # CGPoint _adjustedDecelerationTarget                               256 (0x100) / 8       256 (0x100) / 8       432 (0x1B0) / 16      432 (0x1B0) / 16
    # CGSize _adjustedDecelerationFactor                                264 (0x108) / 8       264 (0x108) / 8       448 (0x1C0) / 16      448 (0x1C0) / 16
    # double _decelerationLnFactorH                                     272 (0x110) / 8       272 (0x110) / 8       464 (0x1D0) / 8       464 (0x1D0) / 8
    # double _decelerationLnFactorV                                     280 (0x118) / 8       280 (0x118) / 8       472 (0x1D8) / 8       472 (0x1D8) / 8
    # id * _shadows                                                     288 (0x120) / 4       288 (0x120) / 4       480 (0x1E0) / 8       480 (0x1E0) / 8
    # id _scrollNotificationViews                                       292 (0x124) / 4       292 (0x124) / 4       488 (0x1E8) / 8       488 (0x1E8) / 8
    # double _contentOffsetAnimationDuration                            296 (0x128) / 8       296 (0x128) / 8       496 (0x1F0) / 8       496 (0x1F0) / 8
    # id _animation                                                     304 (0x130) / 4       304 (0x130) / 4       504 (0x1F8) / 8       504 (0x1F8) / 8
    # id _zoomAnimation                                                 308 (0x134) / 4       308 (0x134) / 4       512 (0x200) / 8       512 (0x200) / 8
    # id _pinch                                                         312 (0x138) / 4       312 (0x138) / 4       520 (0x208) / 8       520 (0x208) / 8
    # id _pan                                                           316 (0x13C) / 4       316 (0x13C) / 4       528 (0x210) / 8       528 (0x210) / 8
    # id _swipe                                                         320 (0x140) / 4       320 (0x140) / 4       536 (0x218) / 8       536 (0x218) / 8
    # id _touchDelayGestureRecognizer                                   324 (0x144) / 4       324 (0x144) / 4       544 (0x220) / 8       544 (0x220) / 8
    # UISwipeGestureRecognizer *[4] _lowFidelitySwipeGestureRecognizers 328 (0x148) / 16      328 (0x148) / 16      552 (0x228) / 32      552 (0x228) / 32
    # UIScrollView * _draggingChildScrollView                           344 (0x158) / 4       344 (0x158) / 4       584 (0x248) / 8       584 (0x248) / 8
    # CGPoint _parentAdjustment                                         348 (0x15C) / 8       348 (0x15C) / 8       592 (0x250) / 16      592 (0x250) / 16
    # CGFloat _pagingSpringPull                                         356 (0x164) / 4       356 (0x164) / 4       608 (0x260) / 8       608 (0x260) / 8
    # CGFloat _pagingFriction                                           360 (0x168) / 4       360 (0x168) / 4       616 (0x268) / 8       616 (0x268) / 8
    # NSInteger _fastScrollCount                                        364 (0x16C) / 4       364 (0x16C) / 4       624 (0x270) / 8       624 (0x270) / 8
    # CGFloat _fastScrollMultiplier                                     368 (0x170) / 4       368 (0x170) / 4       632 (0x278) / 8       632 (0x278) / 8
    # CGFloat _fastScrollStartMultiplier                                372 (0x174) / 4       372 (0x174) / 4       640 (0x280) / 8       640 (0x280) / 8
    # double _fastScrollEndTime                                         376 (0x178) / 8       376 (0x178) / 8       648 (0x288) / 8       648 (0x288) / 8
    # CGPoint _rotationCenterPoint                                      384 (0x180) / 8       384 (0x180) / 8       656 (0x290) / 16      656 (0x290) / 16
    # CGFloat _accuracy                                                 392 (0x188) / 4       392 (0x188) / 4       672 (0x2A0) / 8       672 (0x2A0) / 8
    # NSUInteger _zoomAnimationCount                                    396 (0x18C) / 4       396 (0x18C) / 4       680 (0x2A8) / 8       680 (0x2A8) / 8
    # CGSize _accumulatedOffset                                         400 (0x190) / 8       400 (0x190) / 8       688 (0x2B0) / 16      688 (0x2B0) / 16
    # NSInteger _touchLevel                                             408 (0x198) / 4       408 (0x198) / 4       704 (0x2C0) / 8       704 (0x2C0) / 8
    # CGFloat _savedKeyboardAdjustmentDelta                             412 (0x19C) / 4       412 (0x19C) / 4       712 (0x2C8) / 8       712 (0x2C8) / 8
    # struct {
    #         unsigned int tracking:1;
    #         unsigned int dragging:1;
    #         unsigned int verticalBounceEnabled:1;
    #         unsigned int horizontalBounceEnabled:1;
    #         unsigned int verticalBouncing:1;
    #         unsigned int horizontalBouncing:1;
    #         unsigned int bouncesZoom:1;
    #         unsigned int zoomBouncing:1;
    #         unsigned int alwaysBounceHorizontal:1;
    #         unsigned int alwaysBounceVertical:1;
    #         unsigned int preventScrollingContainer:1;
    #         unsigned int canCancelContentTouches:1;
    #         unsigned int delaysContentTouches:1;
    #         unsigned int programmaticScrollDisabled:1;
    #         unsigned int scrollDisabled:1;
    #         unsigned int zoomDisabled:1;
    #         unsigned int scrollTriggered:1;
    #         unsigned int showsHorizontalScrollIndicator:1;
    #         unsigned int showsVerticalScrollIndicator:1;
    #         unsigned int indicatorStyle:2;
    #         unsigned int inZoom:1;
    #         unsigned int hideIndicatorsInZoom:1;
    #         unsigned int pushedTrackingMode:1;
    #         unsigned int displayingScrollIndicators:1;
    #         unsigned int verticalIndicatorShrunk:1;
    #         unsigned int horizontalIndicatorShrunk:1;
    #         unsigned int contentFitDisableScrolling:1;
    #         unsigned int pagingEnabled:1;
    #         unsigned int pagingLeft:1;
    #         unsigned int pagingRight:1;
    #         unsigned int pagingUp:1;
    #         unsigned int pagingDown:1;
    #         unsigned int lastHorizontalDirection:1;
    #         unsigned int lastVerticalDirection:1;
    #         unsigned int dontScrollToTop:1;
    #         unsigned int scrollingToTop:1;
    #         unsigned int singleFingerPan:1;
    #         unsigned int autoscrolling:1;
    #         unsigned int automaticContentOffsetAdjustmentDisabled:1;
    #         unsigned int skipStartOffsetAdjustment:1;
    #         unsigned int delegateScrollViewDidScroll:1;
    #         unsigned int delegateScrollViewDidZoom:1;
    #         unsigned int delegateContentSizeForZoomScale:1;
    #         unsigned int preserveCenterDuringRotation:1;
    #         unsigned int delaysTrackingWhileDecelerating:1;
    #         unsigned int pinnedZoomMin:1;
    #         unsigned int pinnedXMin:1;
    #         unsigned int pinnedYMin:1;
    #         unsigned int pinnedXMax:1;
    #         unsigned int pinnedYMax:1;
    #         unsigned int skipLinkChecks:1;
    #         unsigned int staysCenteredDuringPinch:1;
    #         unsigned int wasDelayingPinchForSystemGestures:1;
    #         unsigned int systemGesturesRecognitionPossible:1;
    #         unsigned int disableContentOffsetRounding:1;
    #         unsigned int adjustedDecelerationTargetX:1;
    #         unsigned int adjustedDecelerationTargetY:1;
    #         unsigned int hasScrolled:1;
    #         unsigned int wantsConstrainedContentSize:1;
    #         unsigned int updateInsetBottom:1;
    #         unsigned int beingDraggedByChildScrollView:1;
    #         unsigned int adjustsTargetsOnContentOffsetChanges:1;
    #         unsigned int forwardsTouchesUpResponderChain:1;
    #     } _scrollViewFlags                                            416 (0x1A0) / 8       416 (0x1A0) / 8       720 (0x2D0) / 8       720 (0x2D0) / 8
    # BOOL _useContentDimensionVariablesForConstraintLowering           424 (0x1A8) / 1  + 3  424 (0x1A8) / 1  + 3  728 (0x2D8) / 1  + 7  728 (0x2D8) / 1  + 7
    # id _scrollTestParameters                                          428 (0x1AC) / 4       428 (0x1AC) / 4       736 (0x2E0) / 8       736 (0x2E0) / 8
    # NSInteger _keyboardDismissMode                                    432 (0x1B0) / 4       432 (0x1B0) / 4       744 (0x2E8) / 8       744 (0x2E8) / 8
    # NSISVariable * _contentWidthVariable                              436 (0x1B4) / 4       436 (0x1B4) / 4       752 (0x2F0) / 8       752 (0x2F0) / 8
    # NSISVariable * _contentHeightVariable                             440 (0x1B8) / 4       440 (0x1B8) / 4       760 (0x2F8) / 8       760 (0x2F8) / 8
    # NSArray * _automaticContentConstraints                            444 (0x1BC) / 4       444 (0x1BC) / 4       768 (0x300) / 8       768 (0x300) / 8
    # CADoublePoint _zoomAnchorPoint                                    448 (0x1C0) / 16      448 (0x1C0) / 16      776 (0x308) / 16      776 (0x308) / 16

    def __init__(self, value_obj, internal_dict):
        super(UIScrollView_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIScrollView"

        self.content_size = None
        self.content_inset = None
        self.minimum_zoom_scale = None
        self.maximum_zoom_scale = None

    def get_content_size(self):
        if self.content_size:
            return self.content_size

        self.content_size = self.get_child_value("_contentSize")
        return self.content_size

    def get_content_size_provider(self):
        content_size = self.get_content_size()
        return CGSize.CGSize_SynthProvider(content_size, self.internal_dict)

    def get_content_inset(self):
        if self.content_inset:
            return self.content_inset

        self.content_inset = self.get_child_value("_contentInset")
        return self.content_inset

    def get_minimum_zoom_scale(self):
        if self.minimum_zoom_scale:
            return self.minimum_zoom_scale

        self.minimum_zoom_scale = self.get_child_value("_minimumZoomScale")
        return self.minimum_zoom_scale

    def get_maximum_zoom_scale(self):
        if self.maximum_zoom_scale:
            return self.maximum_zoom_scale

        self.maximum_zoom_scale = self.get_child_value("_maximumZoomScale")
        return self.maximum_zoom_scale

    def summary(self):
        content_size = self.get_content_size()
        content_size_w = self.get_content_size_provider().get_width_value()
        content_size_h = self.get_content_size_provider().get_height_value()
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
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIScrollView_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIScrollView.UIScrollView_SummaryProvider \
                            --category UIKit \
                            UIScrollView")
    debugger.HandleCommand("type category enable UIKit")
