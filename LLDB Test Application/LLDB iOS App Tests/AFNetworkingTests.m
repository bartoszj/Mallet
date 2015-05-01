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

- (void)testAFURLConnectionOperation02
{
    NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"http://www.google.con"]];
    AFURLConnectionOperation *urlOperation = [[AFURLConnectionOperation alloc] initWithRequest:request];
    [self compareObject:urlOperation ofType:@"AFURLConnectionOperation *" toSummary:@"Ready, request={http://www.google.con}"];
    __weak typeof(urlOperation) weakUrlOperation = urlOperation;
    
    XCTestExpectation *exceptation = [self expectationWithDescription:@"Get"];
    
    [urlOperation setCompletionBlock:^{
        [self compareObject:weakUrlOperation ofType:@"AFURLConnectionOperation *" toSummary:@"Finished, request={http://www.google.con}"];
        [exceptation fulfill];
    }];
    [urlOperation start];
    [self compareObject:urlOperation ofType:@"AFURLConnectionOperation *" toSummary:@"Executing, request={http://www.google.con}"];
    
    [self waitForExpectationsWithTimeout:2 handler:nil];
}

#pragma mark - AFHTTPRequestOperation
- (void)testAFHTTPRequestOperation01
{
    NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"http://www.google.com"]];
    AFHTTPRequestOperation *httpOperation = [[AFHTTPRequestOperation alloc] initWithRequest:request];
    [self compareObject:httpOperation ofType:@"AFHTTPRequestOperation *" toSummary:@"Ready, request={http://www.google.com}"];
    __weak typeof(httpOperation) weakHttpOperation = httpOperation;
    
    XCTestExpectation *exceptation = [self expectationWithDescription:@"Get"];
    
    [httpOperation setCompletionBlockWithSuccess:^(AFHTTPRequestOperation *operation, id responseObject) {
        NSString *summary = [NSString stringWithFormat:@"Finished, responseData=%lu bytes, request={http://www.google.com}, response={%@}", (unsigned long)weakHttpOperation.responseData.length, weakHttpOperation.response.URL.absoluteString];
        [self compareObject:weakHttpOperation ofType:@"AFHTTPRequestOperation *" toSummary:summary];
        [exceptation fulfill];
    } failure:nil];
    
    [httpOperation start];
    [self compareObject:httpOperation ofType:@"AFHTTPRequestOperation *" toSummary:@"Executing, request={http://www.google.com}"];
    
    [self waitForExpectationsWithTimeout:2 handler:nil];
}

- (void)testAFHTTPRequestOperation02
{
    NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"http://www.google.con"]];
    AFHTTPRequestOperation *httpOperation = [[AFHTTPRequestOperation alloc] initWithRequest:request];
    [self compareObject:httpOperation ofType:@"AFHTTPRequestOperation *" toSummary:@"Ready, request={http://www.google.con}"];
    __weak typeof(httpOperation) weakHttpOperation = httpOperation;
    
    XCTestExpectation *exceptation = [self expectationWithDescription:@"Get"];
    
    [httpOperation setCompletionBlockWithSuccess:nil failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        [self compareObject:weakHttpOperation ofType:@"AFHTTPRequestOperation *" toSummary:@"Finished, request={http://www.google.con}"];
        [exceptation fulfill];
    }];
    
    [httpOperation start];
    [self compareObject:httpOperation ofType:@"AFHTTPRequestOperation *" toSummary:@"Executing, request={http://www.google.con}"];
    
    [self waitForExpectationsWithTimeout:2 handler:nil];
}

#pragma mark - AFHTTPRequestOperationManager
- (void)testAFHTTPRequestOperationManager01
{
    NSURL *url = [NSURL URLWithString:@"http://api.openweathermap.org/data/2.5/"];
    AFHTTPRequestOperationManager *manager = [[AFHTTPRequestOperationManager alloc] initWithBaseURL:url];
    manager.requestSerializer.timeoutInterval = 123;
    [self compareObject:manager ofType:@"AFHTTPRequestOperationManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/, operations=0, executing=0"];
    
    __weak typeof(manager) weakManager = manager;
    XCTestExpectation *exceptation = [self expectationWithDescription:@"Get"];
    
    [manager GET:@"weather?q=London,uk" parameters:nil success:^(AFHTTPRequestOperation *operation, id responseObject) {
        [self compareObject:weakManager ofType:@"AFHTTPRequestOperationManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/, operations=0, executing=0"];
        [exceptation fulfill];
    } failure:nil];
    
    [self compareObject:manager ofType:@"AFHTTPRequestOperationManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/, operations=1, executing=1"];
    [self waitForExpectationsWithTimeout:2 handler:nil];
}

- (void)testAFHTTPRequestOperationManager02
{
    NSURL *url = [NSURL URLWithString:@"http://api.openweathermap.org/data/2.5/"];
    AFHTTPRequestOperationManager *manager = [[AFHTTPRequestOperationManager alloc] initWithBaseURL:url];
    [self compareObject:manager ofType:@"AFHTTPRequestOperationManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/, operations=0, executing=0"];
    
    __weak typeof(manager) weakManager = manager;
    XCTestExpectation *exceptation = [self expectationWithDescription:@"Get"];
    
    [manager GET:@"" parameters:nil success:nil failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        [self compareObject:weakManager ofType:@"AFHTTPRequestOperationManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/, operations=0, executing=0"];
        [exceptation fulfill];
    }];
    
    [self compareObject:manager ofType:@"AFHTTPRequestOperationManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/, operations=1, executing=1"];
    [self waitForExpectationsWithTimeout:2 handler:nil];
}

#pragma mark - AFHTTPRequestSerializer
- (void)testAFHTTPRequestSerializer01
{
    AFHTTPRequestSerializer *serializer = [AFHTTPRequestSerializer serializer];
    serializer.timeoutInterval = 34;
    [self compareObject:serializer ofType:@"AFHTTPRequestSerializer *" toSummary:@"timeout=34"];
    
    serializer.stringEncoding = NSUTF16StringEncoding;
    [self compareObject:serializer ofType:@"AFHTTPRequestSerializer *" toSummary:@"stringEncoding=UTF16, timeout=34"];
    
    serializer.timeoutInterval = 0;
    serializer.allowsCellularAccess = YES;
    [self compareObject:serializer ofType:@"AFHTTPRequestSerializer *" toSummary:@"stringEncoding=UTF16, allowsCellularAccess"];
}

- (void)testAFHTTPRequestSerializer02
{
    AFHTTPRequestSerializer *serializer = [AFHTTPRequestSerializer serializer];
    serializer.cachePolicy = NSURLRequestReturnCacheDataElseLoad;
    [self compareObject:serializer ofType:@"AFHTTPRequestSerializer *" toSummary:@"cachePolicy=ReturnCacheDataElseLoad"];
    
    serializer.HTTPShouldUsePipelining = YES;
    [self compareObject:serializer ofType:@"AFHTTPRequestSerializer *" toSummary:@"cachePolicy=ReturnCacheDataElseLoad, shouldUsePipelining"];
    
    serializer.networkServiceType = NSURLNetworkServiceTypeVideo;
    [self compareObject:serializer ofType:@"AFHTTPRequestSerializer *" toSummary:@"cachePolicy=ReturnCacheDataElseLoad, shouldUsePipelining, networkServiceType=Video"];
}

#pragma mark - AFJSONRequestSerializer
- (void)testAFJSONRequestSerializer01
{
    AFJSONRequestSerializer *serializer = [AFJSONRequestSerializer serializer];
    serializer.writingOptions = NSJSONWritingPrettyPrinted;
    [self compareObject:serializer ofType:@"AFJSONRequestSerializer *" toSummary:@"writingOptions=(PrettyPrinted)"];
    
    serializer.timeoutInterval = 123;
    [self compareObject:serializer ofType:@"AFJSONRequestSerializer *" toSummary:@"writingOptions=(PrettyPrinted), timeout=123"];
}

@end
