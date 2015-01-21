//
//  LLDB_iOS_Test_App_KIF.m
//  LLDB iOS Test App KIF
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <XCTest/XCTest.h>
#import "KIFUITestActor+AlertsAdditions.h"
#import "KIFUITestActor+Application.h"
#import "KIFUITestActor+BasicControllerAdditions.h"
#import "KIFUITestActor+ModalControllerAdditions.h"
#import "KIFUITestActor+ViewControllerAdditions.h"

@interface LLDB_iOS_Test_App_KIF : KIFTestCase

@end

@implementation LLDB_iOS_Test_App_KIF

#pragma mark - Setup
- (void)beforeAll
{
    
}

- (void)beforeEach
{
    [tester app_popToRootViewControllerAnimated:NO];
}

- (void)afterEach
{
    [tester app_popToRootViewControllerAnimated:NO];
}

- (void)afterAll
{
    
}

#pragma mark - Test basic controls
- (void)test01BasicControls
{
    [tester vc_goToBasicControls];
    [tester bvc_tapSomeButtonTextButton];
}

- (void)test02PickersControls
{
    [tester vc_goToPickersControls];
}

- (void)test03AlertsControls
{
    [tester vc_goToAlertsControls];
    [tester waitForTimeInterval:2];
    [tester al_cancelAlert];
}

- (void)test04ViewsControls
{
    [tester vc_goToViewsControls];
}

- (void)test05ScrollViewControls
{
    [tester vc_goToScrollViewControls];
}

- (void)test06ModalControls
{
    [tester vc_goToModalViewControls];
    [tester waitForTimeInterval:2];
    [tester mod_closeModal];
}

@end
