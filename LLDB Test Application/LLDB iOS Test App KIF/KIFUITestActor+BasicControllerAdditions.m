//
//  KIFUITestActor+BasicControllerAdditions.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "KIFUITestActor+BasicControllerAdditions.h"

@implementation KIFUITestActor (BasicControllerAdditions)

- (void)bvc_tapSomeButtonTextButton
{
    [tester tapViewWithAccessibilityLabel:@"Some button text"];
}

@end
