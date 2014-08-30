//
//  QuartzCoreTests.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 30.08.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "SharedTestCase.h"

@interface QuartzCoreTests : SharedTestCase

@end

@implementation QuartzCoreTests

#pragma mark - Setup
- (void)setUp
{
    [super setUp];
    // Put setup code here. This method is called before the invocation of each test method in the class.
}

- (void)tearDown
{
    // Put teardown code here. This method is called after the invocation of each test method in the class.
    [super tearDown];
}

#pragma mark - CALayer
- (void)testCALayer1
{
    CALayer *layer = [CALayer new];
    layer.position = CGPointMake(1, 2);
    layer.bounds = CGRectMake(1, 2, 160, 161);
    
    CompareObjectWithSummary(layer, @"CALayer *", @"position=(1, 2), bounds=(1 2; 160 161)");
}

@end
