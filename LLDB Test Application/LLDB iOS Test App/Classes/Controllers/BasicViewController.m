//
//  BasicViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 29.08.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "BasicViewController.h"

@interface BasicViewController ()

#pragma mark - Properties
@property (weak, nonatomic) IBOutlet UILabel *label;
@property (weak, nonatomic) IBOutlet UILabel *attributedLabel;
@property (weak, nonatomic) IBOutlet UIButton *button;

@end

@implementation BasicViewController

#pragma mark - View life cycle.
- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = @"Basic controls";
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    
    CompareObjectWithSummary(self.label, @"UILabel *", @"text=@\"Label text\"");
    CompareObjectWithSummary(self.attributedLabel, @"UILabel *", @"text=@\"Attributed label text\"");
    CompareObjectWithSummary(self.button, @"UIButton *", @"text=@\"Some button text\"");
}

@end
