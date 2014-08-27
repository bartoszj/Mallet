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
    [self compareObject:d8 ofType:@"NSData *" toSumamry:@"18 bytes"];
}

- (void)testNSData2
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d16 = [s dataUsingEncoding:NSUTF16StringEncoding];
    [self compareObject:d16 ofType:@"NSData *" toSumamry:@"20 bytes"];
}

- (void)testNSData3
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d16l = [s dataUsingEncoding:NSUTF16LittleEndianStringEncoding];
    [self compareObject:d16l ofType:@"NSData *" toSumamry:@"18 bytes"];
}

- (void)testNSData4
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d16b = [s dataUsingEncoding:NSUTF16BigEndianStringEncoding];
    [self compareObject:d16b ofType:@"NSData *" toSumamry:@"18 bytes"];
}

- (void)testNSData5
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d32 = [s dataUsingEncoding:NSUTF32StringEncoding];
    [self compareObject:d32 ofType:@"NSData *" toSumamry:@"40 bytes"];
}

- (void)testNSData6
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d32l = [s dataUsingEncoding:NSUTF32LittleEndianStringEncoding];
    [self compareObject:d32l ofType:@"NSData *" toSumamry:@"36 bytes"];
}

- (void)testNSData7
{
    NSString *s = @"ęóąśłżźćń";
    NSData *d32b = [s dataUsingEncoding:NSUTF32BigEndianStringEncoding];
    [self compareObject:d32b ofType:@"NSData *" toSumamry:@"36 bytes"];
}

#pragma mark - NSUUID
- (void)testNSUUID1
{
    NSUUID *uuid = [[NSUUID alloc] initWithUUIDString:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
    [self compareObject:uuid ofType:@"NSUUID *" toSumamry:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
}

- (void)testNSUUID2
{
    NSUUID *uuid = [[NSUUID alloc] initWithUUIDString:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
    [self compareObject:uuid ofType:@"__NSConcreteUUID *" toSumamry:@"68753A44-4D6F-1226-9C60-0050E4C00067"];
}

#pragma mark - NSURL / NSURLRequest
- (void)testNSURL
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    [self compareObject:url ofType:@"NSURL *" toSumamry:@"@\"https://google.com\""];
}

- (void)testNSURLRequest1
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"url=@\"https://google.com\""];
}

- (void)testNSURLRequest2
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    [self compareObject:request ofType:@"NSMutableURLRequest *" toSumamry:@"url=@\"https://google.com\""];
    
    request.HTTPBody = [@"httpBodyData" dataUsingEncoding:NSUTF8StringEncoding];
    [self compareObject:request ofType:@"NSMutableURLRequest *" toSumamry:@"url=@\"https://google.com\", method=@\"GET\""];
    
    request.HTTPMethod = @"POST";
    [self compareObject:request ofType:@"NSMutableURLRequest *" toSumamry:@"url=@\"https://google.com\", method=@\"POST\""];
}

#pragma mark - NSDateComponents
- (void)testNSDateComponents01
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.era = 1;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"era=1"];
}

- (void)testNSDateComponents02
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.year = 2;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"year=2"];
}

- (void)testNSDateComponents03
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.month = 3;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"month=3"];
}

- (void)testNSDateComponents04
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.day = 4;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"day=4"];
}

- (void)testNSDateComponents05
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.hour = 5;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"hour=5"];
}

- (void)testNSDateComponents06
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.minute = 6;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"minute=6"];
}

- (void)testNSDateComponents07
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.second = 7;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"second=7"];
}

- (void)testNSDateComponents08
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.week = 8;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"week=8"];
}

- (void)testNSDateComponents09
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekday = 9;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"weekday=9"];
}

- (void)testNSDateComponents10
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekdayOrdinal = 10;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"weekdayOrdinal=10"];
}

- (void)testNSDateComponents11
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.quarter = 11;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"quarter=11"];
}

- (void)testNSDateComponents12
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekOfYear = 12;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"weekOfYear=12"];
}

- (void)testNSDateComponents13
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.weekOfMonth = 13;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"weekOfMonth=13"];
}

- (void)testNSDateComponents14
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.yearForWeekOfYear = 14;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"yearForWeekOfYear=14"];
}

- (void)testNSDateComponents15
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.hour = 5;
    dateComponents.minute = 6;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"time=05:06"];
}

- (void)testNSDateComponents16
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.hour = 5;
    dateComponents.minute = 6;
    dateComponents.second = 7;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"time=05:06:07"];
}

- (void)testNSDateComponents17
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.year = 2014;
    dateComponents.month = 3;
    dateComponents.day = 21;
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"date=2014-03-21"];
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
    [self compareObject:dateComponents ofType:@"NSDateComponents *" toSumamry:@"2014-03-21 05:06:07"];
}

@end
