//
//  ModalViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 12.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "ModalViewController.h"

@interface ModalViewController ()

@end

@implementation ModalViewController

#pragma mark - Actions
- (IBAction)closeButtonTouched:(UIBarButtonItem *)sender
{
    [self dismissViewControllerAnimated:YES completion:nil];
}

@end
