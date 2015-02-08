//
//  KIFUITestActor+AlertsAdditions.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "KIFUITestActor+AlertsAdditions.h"

@implementation KIFUITestActor (AlertsAdditions)

- (void)al_cancelAlert
{
    [tester tapViewWithAccessibilityLabel:@"Cancel"];
}

@end
