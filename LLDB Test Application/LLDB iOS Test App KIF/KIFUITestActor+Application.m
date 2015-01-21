//
//  KIFUITestActor+Application.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "KIFUITestActor+Application.h"

@implementation KIFUITestActor (Application)

- (UIWindow *)app_window
{
    UIApplication *app = [UIApplication sharedApplication];
    id<UIApplicationDelegate> appDelegate = app.delegate;
    UIWindow *window = [appDelegate window];
    return window;
}

- (UINavigationController *)app_rootViewController
{
    UIWindow *window = [self app_window];
    UINavigationController *navc = (UINavigationController *)window.rootViewController;
    return navc;
}

- (void)app_popToRootViewControllerAnimated:(BOOL)animated
{
    UINavigationController *navc = [self app_rootViewController];
    [navc popToRootViewControllerAnimated:animated];
}

@end
