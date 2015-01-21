//
//  KIFUITestActor+ViewControllerAdditions.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "KIFUITestActor+ViewControllerAdditions.h"

@implementation KIFUITestActor (ViewControllerAdditions)

- (void)vc_goToBasicControls
{
    [tester tapViewWithAccessibilityLabel:@"Basic controls"];
}

- (void)vc_goToPickersControls
{
    [tester tapViewWithAccessibilityLabel:@"Pickers"];
}

- (void)vc_goToAlertsControls
{
    [tester tapViewWithAccessibilityLabel:@"Alerts"];
}

- (void)vc_goToViewsControls
{
    [tester tapViewWithAccessibilityLabel:@"Views"];
}

- (void)vc_goToScrollViewControls
{
    [tester tapViewWithAccessibilityLabel:@"Scroll view"];
}

- (void)vc_goToModalViewControls
{
    [tester tapViewWithAccessibilityLabel:@"Modal view"];
}

@end
