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
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
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
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
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
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
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
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
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
    [self waitForExpectationsWithTimeout:10 handler:nil];
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
    [self waitForExpectationsWithTimeout:10 handler:nil];
}

#pragma mark - AFURLSessionManager
- (void)testAFURLSessionManager01
{
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    AFURLSessionManager *manager = [[AFURLSessionManager alloc] initWithSessionConfiguration:configuration];
    manager.session.sessionDescription = @"Session Description";
    [self compareObject:manager ofType:@"AFURLSessionManager *" toSummary:@"@\"Session Description\""];
}

#pragma mark - AFHTTPSessionManager
- (void)testAFHTTPSessionManager01
{
    NSURL *url = [NSURL URLWithString:@"http://api.openweathermap.org/data/2.5/"];
    NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
    AFHTTPSessionManager *manager = [[AFHTTPSessionManager alloc] initWithBaseURL:url sessionConfiguration:configuration];
    
    [self compareObject:manager ofType:@"AFHTTPSessionManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/"];
    
    manager.session.sessionDescription = @"Session Description";
    [self compareObject:manager ofType:@"AFHTTPSessionManager *" toSummary:@"baseURL=http://api.openweathermap.org/data/2.5/, @\"Session Description\""];
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

#pragma mark - AFPropertyListRequestSerializer
- (void)testAFPropertyListRequestSerializer01
{
    AFPropertyListRequestSerializer *serializer = [AFPropertyListRequestSerializer serializer];
    [self compareObject:serializer ofType:@"AFPropertyListRequestSerializer *" toSummary:@"format=XML"];
    
    serializer.format = NSPropertyListBinaryFormat_v1_0;
    [self compareObject:serializer ofType:@"AFPropertyListRequestSerializer *" toSummary:@"format=Binary"];
    
    serializer.writeOptions = NSPropertyListMutableContainers;
    [self compareObject:serializer ofType:@"AFPropertyListRequestSerializer *" toSummary:@"format=Binary, writeOptions=MutableContainers"];
    
    serializer.timeoutInterval = 423;
    [self compareObject:serializer ofType:@"AFPropertyListRequestSerializer *" toSummary:@"format=Binary, writeOptions=MutableContainers, timeout=423"];
}

#pragma mark - AFHTTPResponseSerializer
- (void)testAFHTTPResponseSerializer01
{
    AFHTTPResponseSerializer *serializer = [AFHTTPResponseSerializer serializer];
    serializer.stringEncoding = NSUTF32StringEncoding;
    [self compareObject:serializer ofType:@"AFHTTPResponseSerializer *" toSummary:@"stringEncoding=UTF32"];
}

#pragma mark - AFJSONResponseSerializer
- (void)testAFJSONResponseSerializer01
{
    AFJSONResponseSerializer *serializer = [AFJSONResponseSerializer serializer];
    serializer.readingOptions = NSJSONReadingAllowFragments;
    [self compareObject:serializer ofType:@"AFJSONResponseSerializer *" toSummary:@"readingOptions=AllowFragments"];
    
    serializer.removesKeysWithNullValues = YES;
    [self compareObject:serializer ofType:@"AFJSONResponseSerializer *" toSummary:@"readingOptions=AllowFragments, removesKeysWithNullValues"];
    
    serializer.stringEncoding = NSUTF32StringEncoding;
    [self compareObject:serializer ofType:@"AFJSONResponseSerializer *" toSummary:@"readingOptions=AllowFragments, removesKeysWithNullValues, stringEncoding=UTF32"];
}

#pragma mark - AFPropertyListResponseSerializer
- (void)testAFPropertyListResponseSerializer01
{
    AFPropertyListResponseSerializer *serializer = [AFPropertyListResponseSerializer serializer];
    [self compareObject:serializer ofType:@"AFPropertyListResponseSerializer *" toSummary:@"format=XML"];
    
    serializer.format = NSPropertyListBinaryFormat_v1_0;
    [self compareObject:serializer ofType:@"AFPropertyListResponseSerializer *" toSummary:@"format=Binary"];
    
    serializer.readOptions = NSPropertyListMutableContainersAndLeaves;
    [self compareObject:serializer ofType:@"AFPropertyListResponseSerializer *" toSummary:@"format=Binary, readOptions=MutableContainersAndLeaves"];
    
    serializer.stringEncoding = NSASCIIStringEncoding;
    [self compareObject:serializer ofType:@"AFPropertyListResponseSerializer *" toSummary:@"format=Binary, readOptions=MutableContainersAndLeaves, stringEncoding=ASCII"];
}

#pragma mark - AFXMLParserResponseSerializer
- (void)testAFXMLParserResponseSerializer01
{
    AFXMLParserResponseSerializer *serializer = [AFXMLParserResponseSerializer serializer];
    serializer.stringEncoding = NSUTF32StringEncoding;
    [self compareObject:serializer ofType:@"AFXMLParserResponseSerializer *" toSummary:@"stringEncoding=UTF32"];
}

#pragma mark - AFXMLDocumentResponseSerializer
#ifdef __MAC_OS_X_VERSION_MIN_REQUIRED
- (void)testAFXMLDocumentResponseSerializer01
{
    AFXMLDocumentResponseSerializer *serializer = [AFXMLDocumentResponseSerializer serializer];
    serializer.stringEncoding = NSUTF32StringEncoding;
    [self compareObject:serializer ofType:@"AFXMLDocumentResponseSerializer *" toSummary:@"stringEncoding=UTF32"];
}
#endif

#pragma mark - AFImageResponseSerializer
- (void)testAFImageResponseSerializer01
{
    AFImageResponseSerializer *serializer = [AFImageResponseSerializer serializer];
    [self compareObject:serializer ofType:@"AFImageResponseSerializer *" toSummary:@"imageScale=2"];
    
    serializer.imageScale = 3;
    [self compareObject:serializer ofType:@"AFImageResponseSerializer *" toSummary:@"imageScale=3"];
    
    serializer.automaticallyInflatesResponseImage = NO;
    [self compareObject:serializer ofType:@"AFImageResponseSerializer *" toSummary:@"imageScale=3, manuallyInflatesResponseImage"];
    
    serializer.stringEncoding = NSUTF32StringEncoding;
    [self compareObject:serializer ofType:@"AFImageResponseSerializer *" toSummary:@"imageScale=3, manuallyInflatesResponseImage, stringEncoding=UTF32"];
}

#pragma mark - AFCompoundResponseSerializer
- (void)testAFCompoundResponseSerializer01
{
    AFCompoundResponseSerializer *serializer = [AFCompoundResponseSerializer serializer];
    [self compareObject:serializer ofType:@"AFCompoundResponseSerializer *" toSummary:@"serializers=0"];
}

- (void)testAFCompoundResponseSerializer02
{
    AFJSONResponseSerializer *json = [AFJSONResponseSerializer serializer];
    AFXMLParserResponseSerializer *xml = [AFXMLParserResponseSerializer serializer];
    
    AFCompoundResponseSerializer *serializer = [AFCompoundResponseSerializer compoundSerializerWithResponseSerializers:@[json, xml]];
    [self compareObject:serializer ofType:@"AFCompoundResponseSerializer *" toSummary:@"serializers=2"];
}

#pragma mark - AFSecurityPolicy
- (void)testAFSecurityPolicy01
{
    AFSecurityPolicy *policy = [AFSecurityPolicy defaultPolicy];
    [self compareObject:policy ofType:@"AFSecurityPolicy *" toSummary:@"sslPinningMode=None"];
    
    policy.allowInvalidCertificates = YES;
    [self compareObject:policy ofType:@"AFSecurityPolicy *" toSummary:@"allowInvalidCertificates, sslPinningMode=None"];
    
    policy.validatesCertificateChain = NO;
    [self compareObject:policy ofType:@"AFSecurityPolicy *" toSummary:@"allowInvalidCertificates, notValidatesCertificateChain, sslPinningMode=None"];
    
    policy.validatesDomainName = NO;
    [self compareObject:policy ofType:@"AFSecurityPolicy *" toSummary:@"allowInvalidCertificates, notValidatesCertificateChain, notValidatesDomainName, sslPinningMode=None"];
    
    policy.pinnedCertificates = @[[NSData new]];
    [self compareObject:policy ofType:@"AFSecurityPolicy *" toSummary:@"allowInvalidCertificates, notValidatesCertificateChain, notValidatesDomainName, sslPinningMode=None, pinnedCertificates=1"];
}

- (void)testAFSecurityPolicy02
{
    AFSecurityPolicy *policy = [AFSecurityPolicy policyWithPinningMode:AFSSLPinningModeCertificate];
    [self compareObject:policy ofType:@"AFSecurityPolicy *" toSummary:@"sslPinningMode=Certificate"];
}

- (void)testAFSecurityPolicy03
{
    AFSecurityPolicy *policy = [AFSecurityPolicy policyWithPinningMode:AFSSLPinningModePublicKey];
    [self compareObject:policy ofType:@"AFSecurityPolicy *" toSummary:@"sslPinningMode=PublicKey"];
}

#pragma mark - AFNetworkActivityIndicatorManager
- (void)testAFNetworkActivityIndicatorManager01
{
    AFNetworkActivityIndicatorManager *manager = [AFNetworkActivityIndicatorManager sharedManager];
    [self compareObject:manager ofType:@"AFNetworkActivityIndicatorManager *" toSummary:@"disabled"];
    
    manager.enabled = YES;
    [manager incrementActivityCount];
    [self compareObject:manager ofType:@"AFNetworkActivityIndicatorManager *" toSummary:@"activityCount=1"];
    
    manager.enabled = NO;
}

#pragma mark - AFNetworkReachabilityManager
- (void)testAFNetworkReachabilityManager01
{
    AFNetworkReachabilityManager *manager = [AFNetworkReachabilityManager sharedManager];
    [self compareObject:manager ofType:@"AFNetworkReachabilityManager *" toSummary:@"status=Unknown"];
    [manager startMonitoring];
    
    XCTestExpectation *exceptation = [self expectationWithDescription:@"Status"];
    __weak typeof(manager) weakManager = manager;
    [manager setReachabilityStatusChangeBlock:^(AFNetworkReachabilityStatus status) {
        [self compareObject:weakManager ofType:@"AFNetworkReachabilityManager *" toSummary:@"status=ReachableViaWiFi"];
        [exceptation fulfill];
    }];
    
    [self waitForExpectationsWithTimeout:10 handler:nil];
    [self compareObject:manager ofType:@"AFNetworkReachabilityManager *" toSummary:@"status=ReachableViaWiFi"];
}

@end
