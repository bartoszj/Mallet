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
    }
}

@end
