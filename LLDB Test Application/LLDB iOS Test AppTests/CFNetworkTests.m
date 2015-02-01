//
//  CFNetworkTests.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SharedTestCase.h"

@interface CFNetworkTests : SharedTestCase

@end

@implementation CFNetworkTests

- (void)setUp {
    [super setUp];
    // Put setup code here. This method is called before the invocation of each test method in the class.
}

- (void)tearDown {
    // Put teardown code here. This method is called after the invocation of each test method in the class.
    [super tearDown];
}

#pragma mark - NSURLRequest
- (void)testNSURLRequest1
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"https://google.com"];
}

- (void)testNSURLRequest2
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSumamry:@"https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"https://google.com"];
}

- (void)testNSURLRequest3
{
    // HTTP Method.
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    mutableRequest.HTTPMethod = @"POST";
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSumamry:@"POST, https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"POST, https://google.com"];
}

- (void)testNSURLRequest4
{
    // HTTP Body.
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    mutableRequest.HTTPBody = [@"httpBodyData" dataUsingEncoding:NSUTF8StringEncoding];
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSumamry:@"GET, https://google.com, body=12 bytes"];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"GET, https://google.com, body=12 bytes"];
}

- (void)testNSURLRequest5
{
    // HTTP Body.
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    mutableRequest.HTTPBody = [@"test data" dataUsingEncoding:NSUTF8StringEncoding];
    NSURLRequest *request = [mutableRequest copy];
    
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSumamry:@"GET, https://google.com, body=9 bytes"];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"GET, https://google.com, body=9 bytes"];
}

- (void)testNSURLRequest6
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSumamry:@"https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"https://google.com"];
    
    // HTTP headers.
    [mutableRequest setValue:@"headerValue" forHTTPHeaderField:@"headerName"];
    [mutableRequest setValue:@"headerValue2" forHTTPHeaderField:@"headerName2"];
    request = [mutableRequest copy];
    
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSumamry:@"GET, https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSumamry:@"GET, https://google.com"];
}

@end
