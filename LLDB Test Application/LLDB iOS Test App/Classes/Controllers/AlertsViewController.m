//
//  AlertsViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 29.08.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "AlertsViewController.h"

@interface AlertsViewController () <UIAlertViewDelegate>

#pragma mark - Properties
@property (weak, nonatomic) UIAlertView *alertView;

@end

@implementation AlertsViewController

#pragma mark - View life cycle
- (void)viewDidLoad
{
    [super viewDidLoad];
    
    self.title = @"Alerts";
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    
    UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:@"Title" message:@"Message" delegate:self cancelButtonTitle:@"Cancel" otherButtonTitles:nil];
    self.alertView = alertView;
    [self.alertView show];
    CompareObjectWithSummary(alertView, @"UIAlertView *", @"title=@\"Title\", message=@\"Message\", buttons=[@\"Cancel\"]");
    CompareObjectWithSummary(self.alertView, @"UIAlertView *", @"title=@\"Title\", message=@\"Message\", buttons=[@\"Cancel\"]");
}

#pragma mark - UIAlertViewDelegate
- (void)didPresentAlertView:(UIAlertView *)alertView
{
    CompareObjectWithSummary(alertView, @"UIAlertView *", @"title=@\"Title\", message=@\"Message\", buttons=[@\"Cancel\"]");
    CompareObjectWithSummary(self.alertView, @"UIAlertView *", @"title=@\"Title\", message=@\"Message\", buttons=[@\"Cancel\"]");
}

@end
