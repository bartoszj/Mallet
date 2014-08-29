//
//  PickersViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 29.08.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "PickersViewController.h"

@interface PickersViewController () <UIPickerViewDataSource, UIPickerViewDelegate>

#pragma mark - Properties
@property (weak, nonatomic) IBOutlet UIPickerView *pickerView;
@property (weak, nonatomic) IBOutlet UIDatePicker *datePicker;

@end

@implementation PickersViewController

#pragma mark - View life cycle.
- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = @"Pickers";
    
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.year = 2014;
    dateComponents.month = 4;
    dateComponents.day = 22;
    dateComponents.hour = 11;
    dateComponents.minute = 44;
    dateComponents.second = 33;
    self.datePicker.date = [[NSCalendar currentCalendar] dateFromComponents:dateComponents];
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    
    CompareObjectWithSummary(self.datePicker, @"UIDatePicker *", @"era=1, 2014-04-22 11:44:33, leapMonth=NO");
}

#pragma mark - Actions
- (IBAction)datePickerDateChanged:(UIDatePicker *)sender
{
}

#pragma mark - UIPickerViewDataSource
- (NSInteger)numberOfComponentsInPickerView:(UIPickerView *)pickerView
{
    return 3;
}

- (NSInteger)pickerView:(UIPickerView *)pickerView numberOfRowsInComponent:(NSInteger)component
{
    return 100;
}

#pragma mark - UIPickerViewDelegate
- (NSString *)pickerView:(UIPickerView *)pickerView titleForRow:(NSInteger)row forComponent:(NSInteger)component
{
    return [NSString stringWithFormat:@"%d", row];
}


@end
