//
//  ScrollViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 29.08.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "ScrollViewController.h"

@interface ScrollViewController () <UIScrollViewDelegate>

#pragma mark - Properties
@property (weak, nonatomic) IBOutlet UIScrollView *scrollView;

@end

@implementation ScrollViewController

#pragma mark - View life cycle
- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = @"Scroll view";
    self.scrollView.contentSize = CGSizeMake(3000, 1000);
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    
    CompareObjectWithSummary(self.scrollView, @"UIScrollView *", @"contentOffset=(0, -64), contentSize=(3000, 1000), inset=(64, 0, 0, 0)");
}

#pragma mark - UIScrollViewDelegate
- (void)scrollViewDidScroll:(UIScrollView *)scrollView
{
}

@end
