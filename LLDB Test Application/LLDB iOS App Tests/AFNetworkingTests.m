//
//  AFNetworking.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 29.04.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SharedTestCase.h"

@interface AFNetworkingTests : SharedTestCase

@end

@implementation AFNetworkingTests

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

#pragma mark - AFURLConnectionOperation
- (void)testAFURLConnectionOperation01
{
    NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"http://www.google.com"]];
    AFURLConnectionOperation *urlOperation = [[AFURLConnectionOperation alloc] initWithRequest:request];
    [self compareObject:urlOperation ofType:@"AFURLConnectionOperation *" toSummary:@"Ready, request={http://www.google.com}"];
    __weak typeof(urlOperation) weakUrlOperation = urlOperation;
    
    XCTestExpectation *exceptation = [self expectationWithDescription:@"Get"];
    
    [urlOperation setCompletionBlock:^{
        NSString *summary = [NSString stringWithFormat:@"Finished, responseData=%lu bytes, request={http://www.google.com}, response={%@}", (unsigned long)weakUrlOperation.responseData.length, weakUrlOperation.response.URL.absoluteString];
        [self compareObject:weakUrlOperation ofType:@"AFURLConnectionOperation *" toSummary:summary];
        [exceptation fulfill];
    }];
    [urlOperation start];
    [self compareObject:urlOperation ofType:@"AFURLConnectionOperation *" toSummary:@"Executing, request={http://www.google.com}"];
    
    [self waitForExpectationsWithTimeout:2 handler:nil];
}

@end
