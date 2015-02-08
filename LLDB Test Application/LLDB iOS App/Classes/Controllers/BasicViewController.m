//
//  BasicViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 29.08.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "BasicViewController.h"
@import QuartzCore;

@interface BasicViewController ()

#pragma mark - Properties
@property (weak, nonatomic) IBOutlet UILabel *label;
@property (weak, nonatomic) IBOutlet UILabel *attributedLabel;
@property (weak, nonatomic) IBOutlet UIButton *systemButton;
@property (weak, nonatomic) IBOutlet UIButton *plainButton;
@property (weak, nonatomic) IBOutlet UIButton *attributedButton;
@property (weak, nonatomic) IBOutlet UITextField *textField1;
@property (weak, nonatomic) IBOutlet UITextField *textField2;
@property (weak, nonatomic) IBOutlet UITextField *textField3;
@property (weak, nonatomic) IBOutlet UISlider *slider;
@property (weak, nonatomic) IBOutlet UIProgressView *progressView;
@property (weak, nonatomic) IBOutlet UISwitch *switch1;
@property (weak, nonatomic) IBOutlet UISwitch *switch2;
@property (weak, nonatomic) IBOutlet UIStepper *stepper;
@property (weak, nonatomic) IBOutlet UISegmentedControl *segmentedControl;
@property (weak, nonatomic) IBOutlet UIPageControl *pageControl;

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
    CompareObjectWithSummary(self.systemButton, @"UIButton *", @"text=@\"Some button text\"");
    CompareObjectWithSummary(self.plainButton, @"UIButton *", @"text=@\"Some plain button text\"");
    CompareObjectWithSummary(self.attributedButton, @"UIButton *", @"text=@\"Some attributed button text\"");
//    CompareObjectWithSummary(self.textField1, @"UITextField *", @"");
    CompareObjectWithSummary(self.textField2, @"UITextField *", @"placeholder=@\"Some placeholder text\"");
    CompareObjectWithSummary(self.textField3, @"UITextField *", @"text=@\"Some text\", placeholder=@\"With placeholder\"");
    CompareObjectWithSummary(self.slider, @"UISlider *", @"value=13.31, min=0, max=43");
    CompareObjectWithSummary(self.progressView, @"UIProgressView *", @"progress=0.54");
    CompareObjectWithSummary(self.switch1, @"UISwitch *", @"on=YES");
    CompareObjectWithSummary(self.switch2, @"UISwitch *", @"on=NO");
    CompareObjectWithSummary(self.stepper, @"UIStepper *", @"value=20, step=2, min=0, max=100");
    CompareObjectWithSummary(self.segmentedControl, @"UISegmentedControl *", @"selected=1, segments=4");
    CompareObjectWithSummary(self.pageControl, @"UIPageControl *", @"currentPage=2, numberOfPages=5");
}

#pragma mark - Actions
- (IBAction)plainButtonTouched:(UIButton *)sender forEvent:(UIEvent *)event
{
    UITouch *touch = event.allTouches.anyObject;
    CGPoint locationInWindow = [touch locationInView:self.view.window];
    NSNumberFormatter *nf = [[NSNumberFormatter alloc] init];
    nf.maximumFractionDigits = 1;
    nf.minimumFractionDigits = 0;
    NSString *x = [nf stringFromNumber:@(locationInWindow.x)];
    NSString *y = [nf stringFromNumber:@(locationInWindow.y)];
    NSString *touchSummary = [NSString stringWithFormat:@"locationInWindow=(x=%@, y=%@), phase=ended, tapCount=1", x, y];
    CompareObjectWithSummary(touch, @"UITouch *", touchSummary);
    CompareObjectWithSummary(event, @"UIEvent *", @"touches=1");
}

@end
