//
//  ViewsViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 30.08.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "ViewsViewController.h"

@interface ViewsViewController ()

#pragma mark - Properties
@property (weak, nonatomic) IBOutlet UIView *rectView1;

@end

@implementation ViewsViewController

#pragma mark - View life cycle
- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = @"Views";
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    
    CompareObjectWithSummary(self.rectView1, @"UIView *", @"frame=(42 72; 123 157)");
}

@end
