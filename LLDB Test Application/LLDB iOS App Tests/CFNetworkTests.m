//
//  CFNetworkTests.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SharedTestCase.h"

@interface CFNetworkTests : SharedTestCase <NSURLConnectionDataDelegate, NSURLSessionDelegate, NSURLSessionTaskDelegate, NSURLSessionDownloadDelegate>

@property (strong, nonatomic) XCTestExpectation *exceptation;

@end

@implementation CFNetworkTests

#pragma mark - Setup
- (void)setUp
{
    [super setUp];
    // Put setup code here. This method is called before the invocation of each test method in the class.
}

- (void)tearDown
{
    // Put teardown code here. This method is called after the invocation of each test method in the class.
    self.exceptation = nil;
    [super tearDown];
}

#pragma mark - NSURLRequest
- (void)testNSURLRequest1
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    [self compareObject:request ofType:@"NSURLRequest *" toSummary:@"https://google.com"];
}

- (void)testNSURLRequest2
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSummary:@"https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSummary:@"https://google.com"];
}

- (void)testNSURLRequest3
{
    // HTTP Method.
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    mutableRequest.HTTPMethod = @"POST";
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSummary:@"POST, https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSummary:@"POST, https://google.com"];
}

- (void)testNSURLRequest4
{
    // HTTP Body.
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    mutableRequest.HTTPBody = [@"httpBodyData" dataUsingEncoding:NSUTF8StringEncoding];
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSummary:@"GET, https://google.com, body=12 bytes"];
    [self compareObject:request ofType:@"NSURLRequest *" toSummary:@"GET, https://google.com, body=12 bytes"];
}

- (void)testNSURLRequest5
{
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    NSURLRequest *request = [mutableRequest copy];
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSummary:@"https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSummary:@"https://google.com"];
    
    // HTTP headers.
    [mutableRequest setValue:@"headerValue" forHTTPHeaderField:@"headerName"];
    [mutableRequest setValue:@"headerValue2" forHTTPHeaderField:@"headerName2"];
    request = [mutableRequest copy];
    
    [self compareObject:mutableRequest ofType:@"NSMutableURLRequest *" toSummary:@"GET, https://google.com"];
    [self compareObject:request ofType:@"NSURLRequest *" toSummary:@"GET, https://google.com"];
}

#pragma mark - NSURLResponse
- (void)testNSURLResponse01
{
    NSURL *url = [NSURL URLWithString:@"http://api.openweathermap.org/data/2.5/weather?q=London,uk"];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    
    XCTestExpectation *exceptation = [self expectationWithDescription:@"GET"];
    
    [NSURLConnection sendAsynchronousRequest:request queue:[NSOperationQueue mainQueue] completionHandler:^(NSURLResponse *response, NSData *data, NSError *connectionError) {
        
        NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *)response;
        
        [self compareObject:response ofType:@"NSURLResponse *" toSummary:@"http://api.openweathermap.org/data/2.5/weather?q=London,uk"];
        [self compareObject:httpResponse ofType:@"NSHTTPURLResponse *" toSummary:@"http://api.openweathermap.org/data/2.5/weather?q=London,uk"];
        
        [exceptation fulfill];
    }];
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

#pragma mark - NSURLConnection
- (void)testNSURLConnection01
{
    NSURL *url = [NSURL URLWithString:@"http://api.openweathermap.org/data/2.5/weather?q=London,uk"];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    self.exceptation = [self expectationWithDescription:@"GET"];
    
    NSURLConnection *connection = [NSURLConnection connectionWithRequest:request delegate:self];
    [self compareObject:connection ofType:@"NSURLConnection *" toSummary:@"url=http://api.openweathermap.org/data/2.5/weather?q=London,uk"];
    [connection start];
    [self compareObject:connection ofType:@"NSURLConnection *" toSummary:@"url=http://api.openweathermap.org/data/2.5/weather?q=London,uk"];
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

- (void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    [self.exceptation fulfill];
}

#pragma mark - NSURLSessionConfiguration
- (void)testNSURLSessionConfiguration01
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
//    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@""];
    configuration.sharedContainerIdentifier = @"Shared Identifier";
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"sharedContainerIdentifier=@\"Shared Identifier\""];
    configuration.allowsCellularAccess = NO;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"sharedContainerIdentifier=@\"Shared Identifier\", disallowsCellularAccess"];
    configuration.networkServiceType = NSURLNetworkServiceTypeVideo;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"sharedContainerIdentifier=@\"Shared Identifier\", disallowsCellularAccess, networkServiceType=Video"];
}

- (void)testNSURLSessionConfiguration02
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    configuration.timeoutIntervalForRequest = 12;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"timeoutRequest=12"];
    configuration.timeoutIntervalForResource = 32;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"timeoutRequest=12, timeoutResource=32"];
}

- (void)testNSURLSessionConfiguration03
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    configuration.HTTPCookieAcceptPolicy = NSHTTPCookieAcceptPolicyAlways;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"HTTPCookieAcceptPolicy=Always"];
    configuration.HTTPShouldSetCookies = NO;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"dontSetCookies, HTTPCookieAcceptPolicy=Always"];
}

- (void)testNSURLSessionConfiguration04
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    configuration.TLSMinimumSupportedProtocol = kSSLProtocol2;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"TLSMin=SSLv2"];
    configuration.TLSMaximumSupportedProtocol = kDTLSProtocol1;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"TLSMin=SSLv2, TLSMax=DTLSv1"];
}

- (void)testNSURLSessionConfiguration05
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    configuration.requestCachePolicy = NSURLRequestReturnCacheDataElseLoad;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"cachePolicy=ReturnCacheDataElseLoad"];
    configuration.sessionSendsLaunchEvents = YES;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"sessionSendsLaunchEvents, cachePolicy=ReturnCacheDataElseLoad"];
    configuration.discretionary = YES;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"discretionary, sessionSendsLaunchEvents, cachePolicy=ReturnCacheDataElseLoad"];
}

- (void)testNSURLSessionConfiguration06
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    configuration.HTTPMaximumConnectionsPerHost = 123;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"HTTPMaximumConnectionsPerHost=123"];
    configuration.HTTPShouldUsePipelining = YES;
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"shouldUsePipelining, HTTPMaximumConnectionsPerHost=123"];
}

- (void)testNSURLSessionConfiguration07
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration backgroundSessionConfigurationWithIdentifier:@"BackgroundIdentifier"];
    [self compareObject:configuration ofType:@"NSURLSessionConfiguration *" toSummary:@"identifier=@\"BackgroundIdentifier\", sessionSendsLaunchEvents, backgroundSession"];
}

#pragma mark - NSURLSession
- (void)testNSURLSession01
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    NSURLSession *session = [NSURLSession sessionWithConfiguration:configuration];
    session.sessionDescription = @"Session Description";
    
    [self compareObject:session ofType:@"NSURLSession *" toSummary:@"@\"Session Description\""];
}

- (void)testNSURLSession02
{
    NSURLSession *session = [NSURLSession sharedSession];
    [self compareObject:session ofType:@"NSURLSession *" toSummary:@"sharedSession"];
    
    session.sessionDescription = @"Session Description";
    [self compareObject:session ofType:@"NSURLSession *" toSummary:@"sharedSession, @\"Session Description\""];
}

#pragma mark - NSURLSessionTask
- (void)testNSURLSessionTask01
{
    NSURLSession *session = [NSURLSession sharedSession];
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    XCTestExpectation *exceptation = [self expectationWithDescription:@"task"];
    __block NSURLSessionDataTask *dataTask = [session dataTaskWithURL:url completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        
        NSString *summary = [NSString stringWithFormat:@"Completed, received=%lu, request={https://google.com}, response={%@}", (unsigned long)data.length, response.URL.absoluteString];
        [self compareObject:dataTask ofType:@"NSURLSessionTask *" toSummary:summary];
        [self compareObject:dataTask ofType:@"NSURLSessionDataTask *" toSummary:summary];
        [exceptation fulfill];
    }];
    NSString *summary = [NSString stringWithFormat:@"Suspended, request={https://google.com}"];
    [self compareObject:dataTask ofType:@"NSURLSessionTask *" toSummary:summary];
    [self compareObject:dataTask ofType:@"NSURLSessionDataTask *" toSummary:summary];
    [dataTask resume];
    summary = [NSString stringWithFormat:@"Running, request={https://google.com}"];
    [self compareObject:dataTask ofType:@"NSURLSessionTask *" toSummary:summary];
    [self compareObject:dataTask ofType:@"NSURLSessionDataTask *" toSummary:summary];
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

- (void)testNSURLSessionTask02
{
    NSURLSession *session = [NSURLSession sharedSession];
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSMutableURLRequest *mutableRequest = [NSMutableURLRequest requestWithURL:url];
    mutableRequest.HTTPBody = [@"httpBodyData" dataUsingEncoding:NSUTF8StringEncoding];
    XCTestExpectation *exceptation = [self expectationWithDescription:@"task"];
    __block NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:mutableRequest completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        
        NSString *summary = [NSString stringWithFormat:@"Completed, received=%lu/%lu, sent=12/12, request={GET, https://google.com, body=12 bytes}, response={%@}", (unsigned long)data.length, (unsigned long)data.length, response.URL.absoluteString];
        [self compareObject:dataTask ofType:@"NSURLSessionTask *" toSummary:summary];
        [self compareObject:dataTask ofType:@"NSURLSessionDataTask *" toSummary:summary];
        [exceptation fulfill];
    }];
    NSString *summary = [NSString stringWithFormat:@"Suspended, request={GET, https://google.com, body=12 bytes}"];
    [self compareObject:dataTask ofType:@"NSURLSessionTask *" toSummary:summary];
    [self compareObject:dataTask ofType:@"NSURLSessionDataTask *" toSummary:summary];
    [dataTask resume];
    summary = [NSString stringWithFormat:@"Running, request={GET, https://google.com, body=12 bytes}"];
    [self compareObject:dataTask ofType:@"NSURLSessionTask *" toSummary:summary];
    [self compareObject:dataTask ofType:@"NSURLSessionDataTask *" toSummary:summary];
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

- (void)testNSURLSessionTask03
{
    NSURLSession *session = [NSURLSession sharedSession];
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    XCTestExpectation *exceptation = [self expectationWithDescription:@"task"];
    __block NSURLSessionDownloadTask *downloadTask = [session downloadTaskWithURL:url completionHandler:^(NSURL *location, NSURLResponse *response, NSError *error) {
        NSData *data = [NSData dataWithContentsOfURL:location];
        NSString *summary = [NSString stringWithFormat:@"Running, received=%lu, request={https://google.com}, response={%@}, path=@\"%@\"", (unsigned long)data.length, response.URL.absoluteString, location.path];
        [self compareObject:downloadTask ofType:@"NSURLSessionDownloadTask *" toSummary:summary];
        [exceptation fulfill];
    }];
    [downloadTask resume];
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

- (void)testNSURLSessionTask04
{
    NSURLSession *session = [NSURLSession sharedSession];
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    XCTestExpectation *exceptation = [self expectationWithDescription:@"task"];
    
    NSData *data = [@"HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData" dataUsingEncoding:NSUTF8StringEncoding];
    __block NSURLSessionUploadTask *uploadTask = [session uploadTaskWithRequest:request fromData:data completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        NSString *summary = [NSString stringWithFormat:@"Completed, received=%lu/%lu, sent=98/98, request={https://google.com}, response={%@}", (unsigned long)data.length, (unsigned long)data.length, response.URL.absoluteString];
        [self compareObject:uploadTask ofType:@"NSURLSessionUploadTask *" toSummary:summary];
        [exceptation fulfill];
    }];
    NSString *summary = [NSString stringWithFormat:@"Suspended, request={https://google.com}"];
    [self compareObject:uploadTask ofType:@"NSURLSessionUploadTask *" toSummary:summary];
    [uploadTask resume];
    summary = [NSString stringWithFormat:@"Running, request={https://google.com}"];
    [self compareObject:uploadTask ofType:@"NSURLSessionUploadTask *" toSummary:summary];
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

- (void)testNSURLSessionTask05
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration backgroundSessionConfigurationWithIdentifier:@"backgroundSession"];
    NSURLSession *session = [NSURLSession sessionWithConfiguration:configuration delegate:self delegateQueue:[NSOperationQueue mainQueue]];
    NSURL *url = [NSURL URLWithString:@"https://google.com"];
    self.exceptation = [self expectationWithDescription:@"task"];
    NSURLSessionDownloadTask *downloadTask = [session downloadTaskWithURL:url];
    
    NSString *summary = [NSString stringWithFormat:@"Suspended, request={https://google.com}"];
    [self compareObject:downloadTask ofType:@"NSURLSessionDownloadTask *" toSummary:summary];
    [downloadTask resume];
    summary = [NSString stringWithFormat:@"Running, request={https://google.com}"];
    [self compareObject:downloadTask ofType:@"NSURLSessionDownloadTask *" toSummary:summary];
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

- (void)URLSession:(NSURLSession *)session downloadTask:(NSURLSessionDownloadTask *)downloadTask didFinishDownloadingToURL:(NSURL *)location
{
    NSString *summary = [NSString stringWithFormat:@"Running, received=%lu, request={https://google.com}, response={%@}", (unsigned long)downloadTask.countOfBytesReceived, downloadTask.response.URL.absoluteString];
    [self compareObject:downloadTask ofType:@"NSURLSessionDownloadTask *" toSummary:summary];
    
    [self.exceptation fulfill];
}

@end
