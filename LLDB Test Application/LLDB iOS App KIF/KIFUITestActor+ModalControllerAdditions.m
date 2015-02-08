//
//  KIFUITestActor+ModalControllerAdditions.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "KIFUITestActor+ModalControllerAdditions.h"

@implementation KIFUITestActor (ModalControllerAdditions)

- (void)mod_closeModal
{
    [tester tapViewWithAccessibilityLabel:@"Close"];
}

@end
