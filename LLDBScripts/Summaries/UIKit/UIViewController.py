#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Bartosz Janda
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
import UIResponder


class UIViewController_SynthProvider(UIResponder.UIResponder_SynthProvider):
    # Class: UIViewController
    # Super class: UIResponder
    # Protocols: _UIViewServiceDeputy, NSCoding, UIAppearanceContainer
    # Name:                                                                  armv7                 i386                  arm64                 x86_64
    # UIView * _view                                                       4 (0x004) / 4         4 (0x004) / 4         8 (0x008) / 8         8 (0x008) / 8
    # UITabBarItem * _tabBarItem                                           8 (0x008) / 4         8 (0x008) / 4        16 (0x010) / 8        16 (0x010) / 8
    # UINavigationItem * _navigationItem                                  12 (0x00C) / 4        12 (0x00C) / 4        24 (0x018) / 8        24 (0x018) / 8
    # NSArray * _toolbarItems                                             16 (0x010) / 4        16 (0x010) / 4        32 (0x020) / 8        32 (0x020) / 8
    # NSString * _title                                                   20 (0x014) / 4        20 (0x014) / 4        40 (0x028) / 8        40 (0x028) / 8
    # NSString * _nibName                                                 24 (0x018) / 4        24 (0x018) / 4        48 (0x030) / 8        48 (0x030) / 8
    # NSBundle * _nibBundle                                               28 (0x01C) / 4        28 (0x01C) / 4        56 (0x038) / 8        56 (0x038) / 8
    # UIViewController * _parentViewController                            32 (0x020) / 4        32 (0x020) / 4        64 (0x040) / 8        64 (0x040) / 8
    # UIViewController * _childModalViewController                        36 (0x024) / 4        36 (0x024) / 4        72 (0x048) / 8        72 (0x048) / 8
    # UIViewController * _parentModalViewController                       40 (0x028) / 4        40 (0x028) / 4        80 (0x050) / 8        80 (0x050) / 8
    # UIViewController * _previousRootViewController                      44 (0x02C) / 4        44 (0x02C) / 4        88 (0x058) / 8        88 (0x058) / 8
    # UIView * _modalTransitionView                                       48 (0x030) / 4        48 (0x030) / 4        96 (0x060) / 8        96 (0x060) / 8
    # UIResponder * _modalPreservedFirstResponder                         52 (0x034) / 4        52 (0x034) / 4       104 (0x068) / 8       104 (0x068) / 8
    # id _dimmingView                                                     56 (0x038) / 4        56 (0x038) / 4       112 (0x070) / 8       112 (0x070) / 8
    # id _dropShadowView                                                  60 (0x03C) / 4        60 (0x03C) / 4       120 (0x078) / 8       120 (0x078) / 8
    # id _currentAction                                                   64 (0x040) / 4        64 (0x040) / 4       128 (0x080) / 8       128 (0x080) / 8
    # UIStoryboard * _storyboard                                          68 (0x044) / 4        68 (0x044) / 4       136 (0x088) / 8       136 (0x088) / 8
    # NSArray * _storyboardSegueTemplates                                 72 (0x048) / 4        72 (0x048) / 4       144 (0x090) / 8       144 (0x090) / 8
    # NSDictionary * _externalObjectsTableForViewLoading                  76 (0x04C) / 4        76 (0x04C) / 4       152 (0x098) / 8       152 (0x098) / 8
    # NSArray * _topLevelObjectsToKeepAliveFromStoryboard                 80 (0x050) / 4        80 (0x050) / 4       160 (0x0A0) / 8       160 (0x0A0) / 8
    # UIView * _savedHeaderSuperview                                      84 (0x054) / 4        84 (0x054) / 4       168 (0x0A8) / 8       168 (0x0A8) / 8
    # UIView * _savedFooterSuperview                                      88 (0x058) / 4        88 (0x058) / 4       176 (0x0B0) / 8       176 (0x0B0) / 8
    # UIBarButtonItem * _editButtonItem                                   92 (0x05C) / 4        92 (0x05C) / 4       184 (0x0B8) / 8       184 (0x0B8) / 8
    # UISearchDisplayController * _searchDisplayController                96 (0x060) / 4        96 (0x060) / 4       192 (0x0C0) / 8       192 (0x0C0) / 8
    # NSInteger _modalTransitionStyle                                    100 (0x064) / 4       100 (0x064) / 4       200 (0x0C8) / 8       200 (0x0C8) / 8
    # NSInteger _modalPresentationStyle                                  104 (0x068) / 4       104 (0x068) / 4       208 (0x0D0) / 8       208 (0x0D0) / 8
    # NSInteger _lastKnownInterfaceOrientation                           108 (0x06C) / 4       108 (0x06C) / 4       216 (0x0D8) / 8       216 (0x0D8) / 8
    # UIPopoverController * _popoverController                           112 (0x070) / 4       112 (0x070) / 4       224 (0x0E0) / 8       224 (0x0E0) / 8
    # UIView * _containerViewInSheet                                     116 (0x074) / 4       116 (0x074) / 4       232 (0x0E8) / 8       232 (0x0E8) / 8
    # CGSize _contentSizeForViewInPopover                                120 (0x078) / 8       120 (0x078) / 8       240 (0x0F0) / 16      240 (0x0F0) / 16
    # CGSize _formSheetSize                                              128 (0x080) / 8       128 (0x080) / 8       256 (0x100) / 16      256 (0x100) / 16
    # UIScrollView * _recordedContentScrollView                          136 (0x088) / 4       136 (0x088) / 4       272 (0x110) / 8       272 (0x110) / 8
    # CDUnknownBlockType _afterAppearance                                140 (0x08C) / 4       140 (0x08C) / 4       280 (0x118) / 8       280 (0x118) / 8
    # NSInteger _explicitAppearanceTransitionLevel                       144 (0x090) / 4       144 (0x090) / 4       288 (0x120) / 8       288 (0x120) / 8
    # NSArray * _keyCommands                                             148 (0x094) / 4       148 (0x094) / 4       296 (0x128) / 8       296 (0x128) / 8
    # struct {
    #         unsigned int appearState:2;
    #         unsigned int isEditing:1;
    #         unsigned int isPerformingModalTransition:1;
    #         unsigned int hidesBottomBarWhenPushed:1;
    #         unsigned int autoresizesArchivedViewToFullSize:1;
    #         unsigned int viewLoadedFromControllerNib:1;
    #         unsigned int isRootViewController:1;
    #         unsigned int customizesForPresentationInPopover:1;
    #         unsigned int isSuspended:1;
    #         unsigned int wasApplicationFrameAtSuspend:1;
    #         unsigned int wantsFullScreenLayout:1;
    #         unsigned int shouldUseFullScreenLayout:1;
    #         unsigned int allowsAutorotation:1;
    #         unsigned int searchControllerRetained:1;
    #         unsigned int oldModalInPopover:1;
    #         unsigned int isModalInPopover:1;
    #         unsigned int isInWillRotateCallback:1;
    #         unsigned int disallowMixedOrientationPresentations:1;
    #         unsigned int isFinishingModalTransition:1;
    #         unsigned int definesPresentationContext:1;
    #         unsigned int providesPresentationContextTransitionStyle:1;
    #         unsigned int containmentSupport:1;
    #         unsigned int isSettingAppearState:1;
    #         unsigned int isInAnimatedVCTransition:1;
    #         unsigned int presentationIsChanging:1;
    #         unsigned int isBeingPresented:1;
    #         unsigned int containmentIsChanging:1;
    #         unsigned int explicitTransitionIsAppearing:1;
    #         unsigned int disableAppearanceTransitions:1;
    #         unsigned int needsDidMoveCleanup:1;
    #         unsigned int suppressesBottomBar:1;
    #         unsigned int disableRootPromotion:1;
    #         unsigned int interfaceOrientationReentranceGuard:1;
    #         unsigned int isExecutingAfterAppearance:1;
    #         unsigned int rootResignationNeeded:1;
    #         unsigned int shouldSynthesizeSupportedOrientations:1;
    #         unsigned int viewConstraintsNeedUpdateOnAppearance:1;
    #         unsigned int shouldForceNonAnimatedTransition:1;
    #         unsigned int isInCustomTransition:1;
    #         unsigned int usesSharedView:1;
    #         unsigned int extendedLayoutIncludesOpaqueBars:1;
    #         unsigned int automaticallyAdjustInsets:1;
    #         unsigned int previousShouldUnderlapUnderStatusBar:1;
    #         unsigned int freezeShouldUnderlapUnderStatusBar:1;
    #         unsigned int neverResizeRoot:1;
    #     } _viewControllerFlags                                         152 (0x098) / 6  + 2  152 (0x098) / 8       304 (0x130) / 8       304 (0x130) / 8
    # NSInteger _retainCount                                             160 (0x0A0) / 4       160 (0x0A0) / 4       312 (0x138) / 8       312 (0x138) / 8
    # BOOL _ignoreAppSupportedOrientations                               164 (0x0A4) / 1       164 (0x0A4) / 1       320 (0x140) / 1       320 (0x140) / 1
    # BOOL _viewHostsLayoutEngine                                        165 (0x0A5) / 1  + 2  165 (0x0A5) / 1  + 2  321 (0x141) / 1  + 6  321 (0x141) / 1  + 6
    # NSString * _storyboardIdentifier                                   168 (0x0A8) / 4       168 (0x0A8) / 4       328 (0x148) / 8       328 (0x148) / 8
    # id <UIViewControllerTransitioningDelegate> _transitioningDelegate  172 (0x0AC) / 4       172 (0x0AC) / 4       336 (0x150) / 8       336 (0x150) / 8
    # BOOL _modalPresentationCapturesStatusBarAppearance                 176 (0x0B0) / 1  + 3  176 (0x0B0) / 1  + 3  344 (0x158) / 1  + 7  344 (0x158) / 1  + 7
    # NSMutableArray * _childViewControllers                             180 (0x0B4) / 4       180 (0x0B4) / 4       352 (0x160) / 8       352 (0x160) / 8
    # CGFloat _customNavigationInteractiveTransitionDuration             184 (0x0B8) / 4       184 (0x0B8) / 4       360 (0x168) / 8       360 (0x168) / 8
    # CGFloat _customNavigationInteractiveTransitionPercentComplete      188 (0x0BC) / 4       188 (0x0BC) / 4       368 (0x170) / 8       368 (0x170) / 8
    # UITransitionView * _customTransitioningView                        192 (0x0C0) / 4       192 (0x0C0) / 4       376 (0x178) / 8       376 (0x178) / 8
    # CGFloat _navigationControllerContentOffsetAdjustment               196 (0x0C4) / 4       196 (0x0C4) / 4       384 (0x180) / 8       384 (0x180) / 8
    # _UILayoutGuide * _topLayoutGuide                                   200 (0x0C8) / 4       200 (0x0C8) / 4       392 (0x188) / 8       392 (0x188) / 8
    # _UILayoutGuide * _bottomLayoutGuide                                204 (0x0CC) / 4       204 (0x0CC) / 4       400 (0x190) / 8       400 (0x190) / 8
    # NSLayoutConstraint * _topBarInsetGuideConstraint                   208 (0x0D0) / 4       208 (0x0D0) / 4       408 (0x198) / 8       408 (0x198) / 8
    # NSLayoutConstraint * _bottomBarInsetGuideConstraint                212 (0x0D4) / 4       212 (0x0D4) / 4       416 (0x1A0) / 8       416 (0x1A0) / 8
    # UIViewController * _sourceViewControllerIfPresentedViaPopoverSegue 216 (0x0D8) / 4       216 (0x0D8) / 4       424 (0x1A8) / 8       424 (0x1A8) / 8
    # UIViewController * _modalSourceViewController                      220 (0x0DC) / 4       220 (0x0DC) / 4       432 (0x1B0) / 8       432 (0x1B0) / 8
    # UIViewController * _presentedStatusBarViewController               224 (0x0E0) / 4       224 (0x0E0) / 4       440 (0x1B8) / 8       440 (0x1B8) / 8
    # NSUInteger _edgesForExtendedLayout                                 228 (0x0E4) / 4       228 (0x0E4) / 4       448 (0x1C0) / 8       448 (0x1C0) / 8
    # UIView * __embeddedView                                            232 (0x0E8) / 4       232 (0x0E8) / 4       456 (0x1C8) / 8       456 (0x1C8) / 8
    # UIView * __embeddingView                                           236 (0x0EC) / 4       236 (0x0EC) / 4       464 (0x1D0) / 8       464 (0x1D0) / 8
    # id <_UIViewControllerContentViewEmbedding> __embeddedDelegate      240 (0x0F0) / 4       240 (0x0F0) / 4       472 (0x1D8) / 8       472 (0x1D8) / 8
    # CGSize _preferredContentSize                                       244 (0x0F4) / 8       244 (0x0F4) / 8       480 (0x1E0) / 16      480 (0x1E0) / 16
    # UIEdgeInsets _navigationControllerContentInsetAdjustment           252 (0x0FC) / 16      252 (0x0FC) / 16      496 (0x1F0) / 32      496 (0x1F0) / 32
    # UIEdgeInsets _contentOverlayInsets                                 268 (0x10C) / 16      268 (0x10C) / 16      528 (0x210) / 32      528 (0x210) / 32
    # CGRect __embeddedViewFrame                                         284 (0x11C) / 16      284 (0x11C) / 16      560 (0x230) / 32      560 (0x230) / 32

    def __init__(self, value_obj, internal_dict):
        super(UIViewController_SynthProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIViewController"

        self.title = None

    @Helpers.save_parameter("title")
    def get_title(self):
        return self.get_child_value("_title")

    def get_title_value(self):
        return self.get_summary_value(self.get_title())

    def get_title_summary(self):
        title_value = self.get_title_value()
        return None if title_value is None else "title={}".format(title_value)

    def summary(self):
        title_summary = self.get_title_summary()

        summaries = []
        if title_summary:
            summaries.append(title_summary)

        summary = ", ".join(summaries)
        return summary


def UIViewController_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIViewController_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIViewController.UIViewController_SummaryProvider \
                            --category UIKit \
                            UIViewController")
    debugger.HandleCommand("type category enable UIKit")
