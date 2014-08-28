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
    # UIViewController:
    # Offset / size + alignment (+ arch alignment)                          armv7:                  arm64:
    #
    # UIView *_view                                                           4 = 0x04 / 4            8 = 0x08 / 8
    # UITabBarItem *_tabBarItem                                               8 = 0x08 / 4           16 = 0x10 / 8
    # UINavigationItem *_navigationItem                                      12 = 0x0c / 4           24 = 0x18 / 8
    # NSArray *_toolbarItems                                                 16 = 0x10 / 4           32 = 0x20 / 8
    # NSString *_title                                                       20 = 0x14 / 4           40 = 0x28 / 8
    # NSString *_nibName                                                     24 = 0x18 / 4           48 = 0x30 / 8
    # NSBundle *_nibBundle                                                   28 = 0x1c / 4           56 = 0x38 / 8
    # UIViewController *_parentViewController                                32 = 0x20 / 4           64 = 0x40 / 8
    # UIViewController *_childModalViewController                            36 = 0x24 / 4           72 = 0x48 / 8
    # UIViewController *_parentModalViewController                           40 = 0x28 / 4           80 = 0x50 / 8
    # UIViewController *_previousRootViewController                          44 = 0x2c / 4           88 = 0x58 / 8
    # UIView *_modalTransitionView                                           48 = 0x30 / 4           96 = 0x60 / 8
    # UIResponder *_modalPreservedFirstResponder                             52 = 0x34 / 4          104 = 0x68 / 8
    # id _dimmingView                                                        56 = 0x38 / 4          112 = 0x70 / 8
    # id _dropShadowView                                                     60 = 0x3c / 4          120 = 0x78 / 8
    # id _currentAction                                                      64 = 0x40 / 4          128 = 0x80 / 8
    # UIStoryboard *_storyboard                                              68 = 0x44 / 4          136 = 0x88 / 8
    # NSArray *_storyboardSegueTemplates                                     72 = 0x48 / 4          144 = 0x90 / 8
    # NSDictionary *_externalObjectsTableForViewLoading                      76 = 0x4c / 4          152 = 0x98 / 8
    # NSArray *_topLevelObjectsToKeepAliveFromStoryboard                     80 = 0x50 / 4          160 = 0xa0 / 8
    # UIView *_savedHeaderSuperview                                          84 = 0x54 / 4          168 = 0xa8 / 8
    # UIView *_savedFooterSuperview                                          88 = 0x58 / 4          176 = 0xb0 / 8
    # UIBarButtonItem *_editButtonItem                                       92 = 0x5c / 4          184 = 0xb8 / 8
    # UISearchDisplayController *_searchDisplayController                    96 = 0x60 / 4          192 = 0xc0 / 8
    # NSInteger _modalTransitionStyle                                       100 = 0x64 / 4          200 = 0xc8 / 8
    # NSInteger _modalPresentationStyle                                     104 = 0x68 / 4          208 = 0xd0 / 8
    # NSInteger _lastKnownInterfaceOrientation                              108 = 0x6c / 4          216 = 0xd8 / 8
    # UIPopoverController *_popoverController                               112 = 0x70 / 4          224 = 0xe0 / 8
    # UIView *_containerViewInSheet                                         116 = 0x74 / 4          232 = 0xe8 / 8
    # struct CGSize _contentSizeForViewInPopover                            120 = 0x78 / 8          240 = 0xf0 / 16
    # struct CGSize _formSheetSize                                          128 = 0x80 / 8          256 = 0x100 / 16
    # UIScrollView *_recordedContentScrollView                              136 = 0x88 / 4          272 = 0x110 / 8
    # CDUnknownBlockType _afterAppearance                                   140 = 0x8c / 4          280 = 0x118 / 8
    # NSInteger _explicitAppearanceTransitionLevel                          144 = 0x90 / 4          288 = 0x120 / 8
    # NSArray *_keyCommands                                                 148 = 0x94 / 4          296 = 0x128 / 8
    # struct {
    #     unsigned int appearState:2;
    #     unsigned int isEditing:1;
    #     unsigned int isPerformingModalTransition:1;
    #     unsigned int hidesBottomBarWhenPushed:1;
    #     unsigned int autoresizesArchivedViewToFullSize:1;
    #     unsigned int viewLoadedFromControllerNib:1;
    #     unsigned int isRootViewController:1;
    #     unsigned int customizesForPresentationInPopover:1;
    #     unsigned int isSuspended:1;
    #     unsigned int wasApplicationFrameAtSuspend:1;
    #     unsigned int wantsFullScreenLayout:1;
    #     unsigned int shouldUseFullScreenLayout:1;
    #     unsigned int allowsAutorotation:1;
    #     unsigned int searchControllerRetained:1;
    #     unsigned int oldModalInPopover:1;
    #     unsigned int isModalInPopover:1;
    #     unsigned int isInWillRotateCallback:1;
    #     unsigned int disallowMixedOrientationPresentations:1;
    #     unsigned int isFinishingModalTransition:1;
    #     unsigned int definesPresentationContext:1;
    #     unsigned int providesPresentationContextTransitionStyle:1;
    #     unsigned int containmentSupport:1;
    #     unsigned int isSettingAppearState:1;
    #     unsigned int isInAnimatedVCTransition:1;
    #     unsigned int presentationIsChanging:1;
    #     unsigned int isBeingPresented:1;
    #     unsigned int containmentIsChanging:1;
    #     unsigned int explicitTransitionIsAppearing:1;
    #     unsigned int disableAppearanceTransitions:1;
    #     unsigned int needsDidMoveCleanup:1;
    #     unsigned int suppressesBottomBar:1;
    #     unsigned int disableRootPromotion:1;
    #     unsigned int interfaceOrientationReentranceGuard:1;
    #     unsigned int isExecutingAfterAppearance:1;
    #     unsigned int rootResignationNeeded:1;
    #     unsigned int shouldSynthesizeSupportedOrientations:1;
    #     unsigned int viewConstraintsNeedUpdateOnAppearance:1;
    #     unsigned int shouldForceNonAnimatedTransition:1;
    #     unsigned int isInCustomTransition:1;
    #     unsigned int usesSharedView:1;
    #     unsigned int extendedLayoutIncludesOpaqueBars:1;
    #     unsigned int automaticallyAdjustInsets:1;
    #     unsigned int previousShouldUnderlapUnderStatusBar:1;
    #     unsigned int freezeShouldUnderlapUnderStatusBar:1;
    #     unsigned int neverResizeRoot:1;
    # } _viewControllerFlags                                                152 = 0x98 / 6 + 2      304 = 0x130 / 6 + 2
    # NSInteger _retainCount                                                160 = 0xa0 / 4          312 = 0x138 / 8
    # BOOL _ignoreAppSupportedOrientations                                  164 = 0xa4 / 1          320 = 0x140 / 1
    # BOOL _viewHostsLayoutEngine                                           165 = 0xa5 / 1 + 2      321 = 0x141 / 1 + 6
    # NSString *_storyboardIdentifier                                       168 = 0xa8 / 4          328 = 0x148 / 8
    # id <UIViewControllerTransitioningDelegate> _transitioningDelegate     172 = 0xac / 4          336 = 0x150 / 8
    # BOOL _modalPresentationCapturesStatusBarAppearance                    176 = 0xb0 / 1 + 3      344 = 0x158 / 1 + 7
    # NSMutableArray *_childViewControllers                                 180 = 0xb4 / 4          352 = 0x160 / 8
    # CGFloat _customNavigationInteractiveTransitionDuration                184 = 0xb8 / 4          360 = 0x168 / 8
    # CGFloat _customNavigationInteractiveTransitionPercentComplete         188 = 0xbc / 4          368 = 0x170 / 8
    # id <UIViewControllerTransitioningDelegate> _transitionDelegate        192 = 0xc0 / 4          376 = 0x178 / 8
    # UITransitionView *_customTransitioningView                            196 = 0xc4 / 4          384 = 0x180 / 8
    # CGFloat _navigationControllerContentOffsetAdjustment                  200 = 0xc8 / 4          392 = 0x188 / 8
    # _UILayoutGuide *_topLayoutGuide                                       204 = 0xcc / 4          400 = 0x190 / 8
    # _UILayoutGuide *_bottomLayoutGuide                                    208 = 0xd0 / 4          408 = 0x198 / 8
    # NSLayoutConstraint *_topBarInsetGuideConstraint                       212 = 0xd4 / 4          416 = 0x1a0 / 8
    # NSLayoutConstraint *_bottomBarInsetGuideConstraint                    216 = 0xd8 / 4          424 = 0x1a8 / 8
    # UIViewController *_sourceViewControllerIfPresentedViaPopoverSegue     220 = 0xdc / 4          432 = 0x1b0 / 8
    # UIViewController *_modalSourceViewController                          224 = 0xe0 / 4          440 = 0x1b8 / 8
    # UIViewController *_presentedStatusBarViewController                   228 = 0xe4 / 4          448 = 0x1c0 / 8
    # NSUInteger _edgesForExtendedLayout                                    232 = 0xe8 / 4          456 = 0x1c8 / 8
    # UIView *__embeddedView                                                236 = 0xec / 4          464 = 0x1d0 / 8
    # UIView *__embeddingView                                               240 = 0xf0 / 4          472 = 0x1d8 / 8
    # id <_UIViewControllerContentViewEmbedding> __embeddedDelegate         244 = 0xf4 / 4          480 = 0x1e0 / 8
    # struct CGSize _preferredContentSize                                   248 = 0xf8 / 8          488 = 0x1e8 / 16
    # struct UIEdgeInsets _navigationControllerContentInsetAdjustment       256 = 0x100 / 16        504 = 0x1f8 / 32
    # struct UIEdgeInsets _contentOverlayInsets                             272 = 0x110 / 16        536 = 0x218 / 32
    # struct CGRect __embeddedViewFrame                                     288 = 0x120 / 16        568 = 0x238 / 32

    def __init__(self, value_obj, internal_dict):
        super(UIViewController_SynthProvider, self).__init__(value_obj, internal_dict)

        self.title = None

    def get_title(self):
        if self.title:
            return self.title

        self.title = self.get_child_value("_title")
        return self.title

    def summary(self):
        title = self.get_title()
        title_value = title.GetSummary()
        title_summary = "title={}".format(title_value)

        summary = None
        if title_value:
            summary = title_summary

        return summary


def UIViewController_SummaryProvider(value_obj, internal_dict):
    return Helpers.generic_summary_provider(value_obj, internal_dict, UIViewController_SynthProvider)


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand("type summary add -F UIViewController.UIViewController_SummaryProvider \
                            --category UIKit \
                            UIViewController")
    debugger.HandleCommand("type category enable UIKit")
