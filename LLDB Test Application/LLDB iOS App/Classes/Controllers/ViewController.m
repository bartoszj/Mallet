//
//  ViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 05.11.2013.
//  Copyright (c) 2013 Bartosz Janda. All rights reserved.
//

#import "ViewController.h"

typedef NS_ENUM (NSInteger, ViewControllerCellId) {
    ViewControllerBasicCellId,
    ViewControllerPickersCellId,
    ViewControllerAlertsCellId,
    ViewControllerViewsCellId,
    ViewControllerScrollViewCellId,
    ViewControllerModalCellId,
    ViewControllerCrashCellId,
    ViewControllerExampleCellId,
};

@interface ViewController () <UITableViewDataSource, UITableViewDelegate>

#pragma mark - Properties
@property (weak, nonatomic) IBOutlet UITableView *tableView;

@property (strong, nonatomic) NSArray *cellIds;

@end

@implementation ViewController

#pragma mark - View life cycle.
- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = @"Selector";
    
    self.cellIds = @[
                     @(ViewControllerBasicCellId),
                     @(ViewControllerPickersCellId),
                     @(ViewControllerAlertsCellId),
                     @(ViewControllerViewsCellId),
                     @(ViewControllerScrollViewCellId),
                     @(ViewControllerModalCellId),
                     @(ViewControllerCrashCellId),
                     @(ViewControllerExampleCellId),
                     ];
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    [super prepareForSegue:segue sender:sender];
}

#pragma mark - UITableViewDataSource
- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return [self.cellIds count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString * const CellIdentifier = @"CellIdentifier";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier forIndexPath:indexPath];
    
    ViewControllerCellId cellId = [self.cellIds[indexPath.row] integerValue];
    switch (cellId) {
        case ViewControllerBasicCellId:
            cell.textLabel.text = @"Basic controls";
            break;
        case ViewControllerPickersCellId:
            cell.textLabel.text = @"Pickers";
            break;
        case ViewControllerAlertsCellId:
            cell.textLabel.text = @"Alerts";
            break;
        case ViewControllerViewsCellId:
            cell.textLabel.text = @"Views";
            break;
        case ViewControllerScrollViewCellId:
            cell.textLabel.text = @"Scroll view";
            break;
        case ViewControllerModalCellId:
            cell.textLabel.text = @"Modal view";
            break;
        case ViewControllerCrashCellId:
            cell.textLabel.text = @"Crash";
            break;
        case ViewControllerExampleCellId:
            cell.textLabel.text = @"Example";
            break;
    }

    return cell;
}

#pragma mark - UITableViewDelegate
- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    [tableView deselectRowAtIndexPath:indexPath animated:YES];

    ViewControllerCellId cellId = [self.cellIds[indexPath.row] integerValue];
    switch (cellId) {
        case ViewControllerBasicCellId:
            [self performSegueWithIdentifier:@"ShowBasicControls" sender:nil];
            break;
        case ViewControllerPickersCellId:
            [self performSegueWithIdentifier:@"ShowPickers" sender:nil];
            break;
        case ViewControllerAlertsCellId:
            [self performSegueWithIdentifier:@"ShowAlerts" sender:nil];
            break;
        case ViewControllerViewsCellId:
            [self performSegueWithIdentifier:@"ShowViews" sender:nil];
            break;
        case ViewControllerScrollViewCellId:
            [self performSegueWithIdentifier:@"ShowScrollView" sender:nil];
            break;
        case ViewControllerModalCellId:
            [self performSegueWithIdentifier:@"ShowModal" sender:nil];
            break;
        case ViewControllerCrashCellId:
        {
            NSArray *list = @[@1, @2, @3];
            NSNumber *n = list[3];
            NSLog(@"%@", n);
            break;
        }
        case ViewControllerExampleCellId:
            [self performSegueWithIdentifier:@"ShowExample" sender:nil];
            break;
    }
}

@end
