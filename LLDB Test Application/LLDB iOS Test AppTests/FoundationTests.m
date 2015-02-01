//
//  FoundationTests.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 19.07.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "SharedTestCase.h"

@interface FoundationTests : SharedTestCase

@end

@implementation FoundationTests

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

#pragma mark - NSData
- (void)testNSData1
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d8 = [s dataUsingEncoding:NSUTF8StringEncoding];
    [self compareObject:d8 ofType:@"NSData *" toSummary:@"18 bytes"];
}

- (void)testNSData2
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d16 = [s dataUsingEncoding:NSUTF16StringEncoding];
    [self compareObject:d16 ofType:@"NSData *" toSummary:@"20 bytes"];
}

- (void)testNSData3
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d16l = [s dataUsingEncoding:NSUTF16LittleEndianStringEncoding];
    [self compareObject:d16l ofType:@"NSData *" toSummary:@"18 bytes"];
}

- (void)testNSData4
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d16b = [s dataUsingEncoding:NSUTF16BigEndianStringEncoding];
    [self compareObject:d16b ofType:@"NSData *" toSummary:@"18 bytes"];
}

- (void)testNSData5
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d32 = [s dataUsingEncoding:NSUTF32StringEncoding];
    [self compareObject:d32 ofType:@"NSData *" toSummary:@"40 bytes"];
}

- (void)testNSData6
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d32l = [s dataUsingEncoding:NSUTF32LittleEndianStringEncoding];
    [self compareObject:d32l ofType:@"NSData *" toSummary:@"36 bytes"];
}

- (void)testNSData7
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d32b = [s dataUsingEncoding:NSUTF32BigEndianStringEncoding];
    [self compareObject:d32b ofType:@"NSData *" toSummary:@"36 bytes"];
}

#pragma mark - NSUUID
- (void)testNSUUID1
{
    NSUUID *uuid = [[NSUUID alloc] initWithUUIDString:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
    [self compareObject:uuid ofType:@"NSUUID *" toSummary:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
}

- (void)testNSUUID2
{
    NSUUID *uuid = [[NSUUID alloc] initWithUUIDString:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
    [self compareObject:uuid ofType:@"__NSConcreteUUID *" toSummary:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
}

#pragma mark - NSURL / NSURLRequest
- (void)testNSURL
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    [self compareObject:url ofType:@"NSURL *" toSummary:@"@\"https://google.com\""];
}

#pragma mark - NSDateComponents
- (void)testNSDateComponents01
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.era = 1;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"era=1"];
}

- (void)testNSDateComponents02
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.year = 2;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"year=2"];
}

- (void)testNSDateComponents03
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.month = 3;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"month=3"];
}

- (void)testNSDateComponents04
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.day = 4;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"day=4"];
}

- (void)testNSDateComponents05
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.hour = 5;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"hour=5"];
}

- (void)testNSDateComponents06
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.minute = 6;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"minute=6"];
}

- (void)testNSDateComponents07
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.second = 7;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"second=7"];
}

- (void)testNSDateComponents08
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.week = 8;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"week=8"];
}

- (void)testNSDateComponents09
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekday = 9;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"weekday=9"];
}

- (void)testNSDateComponents10
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekdayOrdinal = 10;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"weekdayOrdinal=10"];
}

- (void)testNSDateComponents11
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.quarter = 11;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"quarter=11"];
}

- (void)testNSDateComponents12
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekOfYear = 12;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"weekOfYear=12"];
}

- (void)testNSDateComponents13
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekOfMonth = 13;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"weekOfMonth=13"];
}

- (void)testNSDateComponents14
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.yearForWeekOfYear = 14;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"yearForWeekOfYear=14"];
}

- (void)testNSDateComponents15
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.hour = 5;
    dateComponents.minute = 6;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"time=05:06"];
}

- (void)testNSDateComponents16
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.hour = 5;
    dateComponents.minute = 6;
    dateComponents.second = 7;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"time=05:06:07"];
}

- (void)testNSDateComponents17
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.year = 2014;
    dateComponents.month = 3;
    dateComponents.day = 21;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"date=2014-03-21"];
}

- (void)testNSDateComponents18
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.year = 2014;
    dateComponents.month = 3;
    dateComponents.day = 21;
    dateComponents.hour = 5;
    dateComponents.minute = 6;
    dateComponents.second = 7;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSummary:@"2014-03-21 05:06:07"];
}

#pragma mark - NSURLComponents
- (void)testNSURLComponents01
{
    NSURLComponents *components = [[NSURLComponents alloc] initWithString:@"http://google.com"];
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"url=\"http://google.com\""];
}

- (void)testNSURLComponents02
{
    NSURLComponents *components = [[NSURLComponents alloc] init];
    components.scheme = @"scheme";
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"scheme=\"scheme\""];
    components.user = @"user";
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"scheme=\"scheme\", user=\"user\""];
    components.password = @"password";
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"scheme=\"scheme\", user=\"user\", password=\"password\""];
}

- (void)testNSURLComponents03
{
    NSURLComponents *components = [[NSURLComponents alloc] init];
    components.host = @"host";
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"host=\"host\""];
    components.port = @(1234);
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"host=\"host\", port=1234"];
    components.path = @"path1/path2";
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"host=\"host\", port=1234, path=\"path1/path2\""];
    components.query = @"query";
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"host=\"host\", port=1234, path=\"path1/path2\", query=\"query\""];
    components.fragment = @"fragment";
    [self compareObject:components ofType:@"NSURLComponents *" toSummary:@"host=\"host\", port=1234, path=\"path1/path2\", query=\"query\", fragment=\"fragment\""];
}

#pragma mark - NSLayoutConstraint
#define NSLayoutConstraintSummaryShort 0
- (void)testNSLayoutConstraint01
{
    UIView *view = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 100, 100)];
    NSLayoutConstraint *constraint1 = [NSLayoutConstraint constraintWithItem:view attribute:NSLayoutAttributeWidth relatedBy:NSLayoutRelationEqual toItem:nil attribute:NSLayoutAttributeNotAnAttribute multiplier:1 constant:200];
    NSLayoutConstraint *constraint2 = [NSLayoutConstraint constraintWithItem:view attribute:NSLayoutAttributeWidth relatedBy:NSLayoutRelationGreaterThanOrEqual toItem:nil attribute:NSLayoutAttributeNotAnAttribute multiplier:1 constant:200];
    NSLayoutConstraint *constraint3 = [NSLayoutConstraint constraintWithItem:view attribute:NSLayoutAttributeHeight relatedBy:NSLayoutRelationLessThanOrEqual toItem:nil attribute:NSLayoutAttributeNotAnAttribute multiplier:1 constant:300];
    
#if !(NSLayoutConstraintSummaryShort)
    intptr_t ptr = (intptr_t)view;
    NSString *summary1 = [NSString stringWithFormat:@"H:[UIView:0x%lx(200)]", ptr];
    NSString *summary2 = [NSString stringWithFormat:@"H:[UIView:0x%lx(>=200)]", ptr];
    NSString *summary3 = [NSString stringWithFormat:@"V:[UIView:0x%lx(<=300)]", ptr];
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSummary:summary1];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSummary:summary2];
    [self compareObject:constraint3 ofType:@"NSLayoutConstraint *" toSummary:summary3];
#else
    // Short version.
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSumamry:@"width == +200"];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSumamry:@"width >= +200"];
    [self compareObject:constraint3 ofType:@"NSLayoutConstraint *" toSumamry:@"height <= +300"];
#endif
}

- (void)testNSLayoutConstraint02
{
    UIView *view = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 100, 100)];
    NSLayoutConstraint *constraint1 = [NSLayoutConstraint constraintWithItem:view attribute:NSLayoutAttributeWidth relatedBy:NSLayoutRelationEqual toItem:nil attribute:NSLayoutAttributeNotAnAttribute multiplier:1 constant:200];
    constraint1.priority = 123;
    NSLayoutConstraint *constraint2 = [NSLayoutConstraint constraintWithItem:view attribute:NSLayoutAttributeWidth relatedBy:NSLayoutRelationGreaterThanOrEqual toItem:nil attribute:NSLayoutAttributeNotAnAttribute multiplier:1 constant:200];
    constraint2.priority = 456;
    NSLayoutConstraint *constraint3 = [NSLayoutConstraint constraintWithItem:view attribute:NSLayoutAttributeHeight relatedBy:NSLayoutRelationLessThanOrEqual toItem:nil attribute:NSLayoutAttributeNotAnAttribute multiplier:1 constant:300];
    constraint3.priority = 789;
    
#if !(NSLayoutConstraintSummaryShort)
    intptr_t ptr = (intptr_t)view;
    NSString *summary1 = [NSString stringWithFormat:@"H:[UIView:0x%lx(200@123)]", ptr];
    NSString *summary2 = [NSString stringWithFormat:@"H:[UIView:0x%lx(>=200@456)]", ptr];
    NSString *summary3 = [NSString stringWithFormat:@"V:[UIView:0x%lx(<=300@789)]", ptr];
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSummary:summary1];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSummary:summary2];
    [self compareObject:constraint3 ofType:@"NSLayoutConstraint *" toSummary:summary3];
#else
    // Short version.
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSumamry:@"width == +200@123"];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSumamry:@"width >= +200@456"];
    [self compareObject:constraint3 ofType:@"NSLayoutConstraint *" toSumamry:@"height <= +300@789"];
#endif
}

- (void)testNSLayoutConstraint03
{
    UIView *view1 = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 100, 100)];
    UIView *view2 = [[UIView alloc] initWithFrame:CGRectMake(10, 20, 300, 400)];
    NSLayoutConstraint *constraint1 = [NSLayoutConstraint constraintWithItem:view1 attribute:NSLayoutAttributeLeft relatedBy:NSLayoutRelationEqual toItem:view2 attribute:NSLayoutAttributeBaseline multiplier:1 constant:-200];
    NSLayoutConstraint *constraint2 = [NSLayoutConstraint constraintWithItem:view1 attribute:NSLayoutAttributeTrailing relatedBy:NSLayoutRelationGreaterThanOrEqual toItem:view2 attribute:NSLayoutAttributeCenterX multiplier:2 constant:200];
    NSLayoutConstraint *constraint3 = [NSLayoutConstraint constraintWithItem:view1 attribute:NSLayoutAttributeTopMargin relatedBy:NSLayoutRelationLessThanOrEqual toItem:view2 attribute:NSLayoutAttributeCenterYWithinMargins multiplier:1 constant:300];
    constraint3.priority = 300;

#if !(NSLayoutConstraintSummaryShort)
    intptr_t ptr1 = (intptr_t)view1;
    intptr_t ptr2 = (intptr_t)view2;
    NSString *summary1 = [NSString stringWithFormat:@"UIView:0x%lx.left == UIView:0x%lx.lastBaseline - 200", ptr1, ptr2];
    NSString *summary2 = [NSString stringWithFormat:@"UIView:0x%lx.trailing >= 2*UIView:0x%lx.centerX + 200", ptr1, ptr2];
    NSString *summary3 = [NSString stringWithFormat:@"UIView:0x%lx.topMargin <= UIView:0x%lx.centerYWithMargins + 300 @300", ptr1, ptr2];
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSummary:summary1];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSummary:summary2];
    [self compareObject:constraint3 ofType:@"NSLayoutConstraint *" toSummary:summary3];
#else
    // Short version.
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSumamry:@"left == lastBaseline-200"];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSumamry:@"trailing >= 2*centerX+200"];
    [self compareObject:constraint3 ofType:@"NSLayoutConstraint *" toSumamry:@"topMargin <= centerYWithMargins+300@300"];
#endif
}

- (void)testNSLayoutConstraint04
{
    UIView *view = [[[UINib nibWithNibName:@"AutolayoutView" bundle:nil] instantiateWithOwner:nil options:nil] firstObject];
    UIView *subView = [view subviews][0];
    NSArray *constraints = [view constraints];
    NSLayoutConstraint *constraint1 = constraints[0];
    NSLayoutConstraint *constraint2 = constraints[1];
    
#if !(NSLayoutConstraintSummaryShort)
    intptr_t ptr1 = (intptr_t)subView;
    intptr_t ptr2 = (intptr_t)view;
    NSString *summary1 = [NSString stringWithFormat:@"UIView:0x%lx.top == UIView:0x%lx.top + standard", ptr1, ptr2];
    NSString *summary2 = [NSString stringWithFormat:@"UIView:0x%lx.leading == UIView:0x%lx.leading + standard", ptr1, ptr2];
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSummary:summary1];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSummary:summary2];
#else
    // Short version.
    [self compareObject:constraint1 ofType:@"NSLayoutConstraint *" toSumamry:@"top == top+standard"];
    [self compareObject:constraint2 ofType:@"NSLayoutConstraint *" toSumamry:@"leading == leading+standard"];
#endif
}

@end
