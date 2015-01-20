//
//  FoundationTests.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 19.07.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "SharedTestCase.h"

@interface CoreGraphicsTests : SharedTestCase

@end

@implementation CoreGraphicsTests

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

#pragma mark - CGPoint
- (void)testCGPoint
{
    CGPoint point = CGPointMake(1, 2);
    [self compareVariable:&point ofType:@"CGPoint *" toSumamry:@"(x=1, y=2)"];
}

#pragma mark - CGSize
- (void)testCGSize
{
    CGSize size = CGSizeMake(3, 4);
    [self compareVariable:&size ofType:@"CGSize *" toSumamry:@"(width=3, height=4)"];
}

#pragma mark - CGRect
- (void)testCGRect
{
    CGRect rect = CGRectMake(6, 7, 8, 9);
    [self compareVariable:&rect ofType:@"CGRect *" toSumamry:@"origin=(x=6, y=7) size=(width=8, height=9)"];
}

#pragma mark - CGVector
- (void)testCGVector
{
    CGVector vector = CGVectorMake(3, 5);
    [self compareVariable:&vector ofType:@"CGVector *" toSumamry:@"(dx=3, dy=5)"];
}

#pragma mark - CGAffineTransform
- (void)testCGAffineTransform
{
    CGAffineTransform transofrm = CGAffineTransformMake(2, 3, 4, 5, 6, 7);
    [self compareVariable:&transofrm ofType:@"CGAffineTransform *" toSumamry:@"[2, 3], [4, 5], [6, 7]"];
}

@end
