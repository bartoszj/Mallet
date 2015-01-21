//
//  KIFUITestActor+Application.h
//  LLDB Test Application
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "KIFUITestActor.h"

@interface KIFUITestActor (Application)

- (UIWindow *)app_window;
- (UINavigationController *)app_rootViewController;
- (void)app_popToRootViewControllerAnimated:(BOOL)animated;

@end
