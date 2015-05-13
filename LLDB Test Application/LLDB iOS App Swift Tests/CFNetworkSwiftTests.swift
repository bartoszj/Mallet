//
//  CFNetworkSwiftTests.swift
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

import UIKit
import XCTest

class CFNetworkSwiftTests: SharedSwiftTestCase, NSURLConnectionDataDelegate, NSURLSessionDelegate, NSURLSessionTaskDelegate, NSURLSessionDownloadDelegate {
    
    var exceptation: XCTestExpectation?

    // MARK: - Setup
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        self.exceptation = nil
        super.tearDown()
    }
    
    //MARK: - NSURLRequest
    func testNSURLRequest1() {
        let url = NSURL(string: "https://google.com")!
        let request = NSURLRequest(URL: url)
        self.compareObject(request, type: "NSURLRequest", summary: "https://google.com")
    }
    
    func testNSURLRequest2() {
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        let request = mutableRequest.copy() as! NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "https://google.com")
    }

    func testNSURLRequest3() {
        // HTTP Method.
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        mutableRequest.HTTPMethod = "POST"
        let request = mutableRequest.copy() as! NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "POST, https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "POST, https://google.com")
    }
    
    func testNSURLRequest4() {
        // HTTP Body.
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        mutableRequest.HTTPBody = "httpBodyData".dataUsingEncoding(NSUTF8StringEncoding)
        let request = mutableRequest.copy() as! NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "GET, https://google.com, body=12 bytes")
        self.compareObject(request, type: "NSURLRequest", summary: "GET, https://google.com, body=12 bytes")
    }
    
    func testNSURLRequest5() {
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        var request = mutableRequest.copy() as! NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "https://google.com")
        
        // HTTP headers.
        mutableRequest.setValue("headerValue", forHTTPHeaderField: "headerName")
        mutableRequest.setValue("headerValue2", forHTTPHeaderField: "headerName2")
        request = mutableRequest.copy() as! NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "GET, https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "GET, https://google.com")
    }

    // MARK: - NSURLResponse
    func testNSURLREsponse01() {
        let url = NSURL(string: "http://api.openweathermap.org/data/2.5/weather?q=London,uk")!
        let request = NSURLRequest(URL: url)
        
        let expectation = self.expectationWithDescription("GET")
        
        NSURLConnection.sendAsynchronousRequest(request, queue: NSOperationQueue.mainQueue()) { (response, data, error) -> Void in
            let httpResponse = response as! NSHTTPURLResponse
            self.compareObject(response, type: "NSURLResponse", summary: "http://api.openweathermap.org/data/2.5/weather?q=London,uk")
            self.compareObject(httpResponse, type: "NSHTTPURLResponse", summary: "http://api.openweathermap.org/data/2.5/weather?q=London,uk")
            
            expectation.fulfill()
        }
        
        self.waitForExpectationsWithTimeout(10, handler: nil)
    }
    
    // MARK: - NSURLConnection
    func testNSURLConnection01() {
        let url = NSURL(string: "http://api.openweathermap.org/data/2.5/weather?q=London,uk")!
        let request = NSURLRequest(URL: url)
        self.exceptation = self.expectationWithDescription("GET")
        
        let connection = NSURLConnection(request: request, delegate: self)!
        self.compareObject(connection, type: "NSURLConnection", summary: "url=http://api.openweathermap.org/data/2.5/weather?q=London,uk")
        connection.start()
        self.compareObject(connection, type: "NSURLConnection", summary: "url=http://api.openweathermap.org/data/2.5/weather?q=London,uk")
        
        self.waitForExpectationsWithTimeout(10, handler: nil)
    }
    
    func connectionDidFinishLoading(connection: NSURLConnection) {
        self.exceptation?.fulfill()
    }
    
    // MARK: - NSURLSessionConfiguration
    func testNSURLSessionConfiguration01() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        configuration.sharedContainerIdentifier = "Shared Identifier"
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "sharedContainerIdentifier=\"Shared Identifier\"")
        configuration.allowsCellularAccess = false
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "sharedContainerIdentifier=\"Shared Identifier\", disallowsCellularAccess")
        configuration.networkServiceType = .NetworkServiceTypeVideo
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "sharedContainerIdentifier=\"Shared Identifier\", disallowsCellularAccess, networkServiceType=Video")
    }
    
    func testNSURLSessionConfiguration02() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        configuration.timeoutIntervalForRequest = 12
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "timeoutRequest=12")
        configuration.timeoutIntervalForResource = 32
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "timeoutRequest=12, timeoutResource=32")
    }
    
    func testNSURLSessionConfiguration03() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        configuration.HTTPCookieAcceptPolicy = .Always
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "HTTPCookieAcceptPolicy=Always")
        configuration.HTTPShouldSetCookies = false
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "dontSetCookies, HTTPCookieAcceptPolicy=Always")
    }
    
    func testNSURLSessionConfiguration04() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        configuration.TLSMinimumSupportedProtocol = kSSLProtocol2
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "TLSMin=SSLv2")
        configuration.TLSMaximumSupportedProtocol = kDTLSProtocol1
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "TLSMin=SSLv2, TLSMax=DTLSv1")
    }
    
    func testNSURLSessionConfiguration05() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        configuration.requestCachePolicy = .ReturnCacheDataElseLoad
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "cachePolicy=ReturnCacheDataElseLoad")
        configuration.sessionSendsLaunchEvents = true
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "sessionSendsLaunchEvents, cachePolicy=ReturnCacheDataElseLoad")
        configuration.discretionary = true
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "discretionary, sessionSendsLaunchEvents, cachePolicy=ReturnCacheDataElseLoad")
    }
    
    func testNSURLSessionConfiguration06() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        configuration.HTTPMaximumConnectionsPerHost = 123
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "HTTPMaximumConnectionsPerHost=123")
        configuration.HTTPShouldUsePipelining = true
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "shouldUsePipelining, HTTPMaximumConnectionsPerHost=123")
    }
    
    func testNSURLSessionConfiguration07() {
        let configuration = NSURLSessionConfiguration.backgroundSessionConfigurationWithIdentifier("BackgroundIdentifier")
        self.compareObject(configuration, type: "NSURLSessionConfiguration", summary: "identifier=\"BackgroundIdentifier\", sessionSendsLaunchEvents, backgroundSession")
    }
    
    // MARK: - NSURLSession
    func testNSURLSession01() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        let session = NSURLSession(configuration: configuration)
        session.sessionDescription = "Session Description"
        self.compareObject(session, type: "NSURLSession", summary: "\"Session Description\"")
    }
    
    func testNSURLSession02() {
        let session = NSURLSession.sharedSession()
        self.compareObject(session, type: "NSURLSession", summary: "sharedSession")
        
        session.sessionDescription = "Session Description"
        self.compareObject(session, type: "NSURLSession", summary: "sharedSession, \"Session Description\"")
    }
    
    // MARK: - NSURLSessionTask
    func testNSURLSessionTask01() {
        let session = NSURLSession.sharedSession()
        let url = NSURL(string: "https://google.com")!
        let exceptation = self.expectationWithDescription("task")
        var dataTask: NSURLSessionDataTask! = nil
        dataTask = session.dataTaskWithURL(url, completionHandler: { (data, response, error) -> Void in
            let summary = "Completed, received=\(data.length), request={https://google.com}, response={\(response.URL!.absoluteString!)}"
            self.compareObject(dataTask, type: "NSURLSessionTask", summary: summary)
            self.compareObject(dataTask, type: "NSURLSessionDataTask", summary: summary)
            exceptation.fulfill()
        })
        var summary = "Suspended, request={https://google.com}"
        self.compareObject(dataTask, type: "NSURLSessionTask", summary: summary)
        self.compareObject(dataTask, type: "NSURLSessionDataTask", summary: summary)
        dataTask.resume()
        summary = "Running, request={https://google.com}"
        self.compareObject(dataTask, type: "NSURLSessionTask", summary: summary)
        self.compareObject(dataTask, type: "NSURLSessionDataTask", summary: summary)
        self.waitForExpectationsWithTimeout(2, handler: nil)
    }
    
    func testNSURLSessionTask02() {
        let session = NSURLSession.sharedSession()
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        mutableRequest.HTTPBody = ("httpBodyData" as NSString).dataUsingEncoding(NSUTF8StringEncoding)
        let exceptation = self.expectationWithDescription("task")
        var dataTask: NSURLSessionDataTask! = nil
        dataTask = session.dataTaskWithRequest(mutableRequest, completionHandler: { (data, response, error) -> Void in
            let summary = "Completed, received=\(data.length)/\(data.length), sent=12/12, request={GET, https://google.com, body=12 bytes}, response={\(response.URL!.absoluteString!)}"
            self.compareObject(dataTask, type: "NSURLSessionTask", summary: summary)
            self.compareObject(dataTask, type: "NSURLSessionDataTask", summary: summary)
            exceptation.fulfill()
        })
        var summary = "Suspended, request={GET, https://google.com, body=12 bytes}"
        self.compareObject(dataTask, type: "NSURLSessionTask", summary: summary)
        self.compareObject(dataTask, type: "NSURLSessionDataTask", summary: summary)
        dataTask.resume()
        summary = "Running, request={GET, https://google.com, body=12 bytes}"
        self.compareObject(dataTask, type: "NSURLSessionTask", summary: summary)
        self.compareObject(dataTask, type: "NSURLSessionDataTask", summary: summary)
        self.waitForExpectationsWithTimeout(2, handler: nil)
    }
    
    func testNSURLSessionTask03() {
        let session = NSURLSession.sharedSession()
        let url = NSURL(string: "https://google.com")!
        let exceptation = self.expectationWithDescription("task")
        var downloadTask: NSURLSessionDownloadTask! = nil
        downloadTask = session.downloadTaskWithURL(url, completionHandler: { (location, response, error) -> Void in
            let data = NSData(contentsOfURL: location)!
            let summary = "Running, received=\(data.length), request={https://google.com}, response={\(response.URL!.absoluteString!)}"
            self.compareObject(downloadTask, type: "NSURLSessionTask", summary: summary)
            exceptation.fulfill()
        })
        downloadTask.resume()
        self.waitForExpectationsWithTimeout(2, handler: nil)
    }
    
    func testNSURLSessionTask04() {
        let session = NSURLSession.sharedSession()
        let url = NSURL(string: "https://google.com")!
        let request = NSURLRequest(URL: url)
        let exceptation = self.expectationWithDescription("task")
        let data = ("HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData, HttpData" as NSString).dataUsingEncoding(NSUTF8StringEncoding)
        var uploadTask: NSURLSessionUploadTask! = nil
        uploadTask = session.uploadTaskWithRequest(request, fromData: data, completionHandler: { (data, response, error) -> Void in
            let summary = "Completed, received=\(data.length)/\(data.length), sent=98/98, request={https://google.com}, response={\(response.URL!.absoluteString!)}"
            self.compareObject(uploadTask, type: "NSURLSessionUploadTask", summary: summary)
            exceptation.fulfill()
        })
        var summary = "Suspended, request={https://google.com}"
        self.compareObject(uploadTask, type: "NSURLSessionUploadTask", summary: summary)
        uploadTask.resume()
        summary = "Running, request={https://google.com}"
        self.compareObject(uploadTask, type: "NSURLSessionUploadTask", summary: summary)
        self.waitForExpectationsWithTimeout(2, handler: nil)
    }
    
    func testNSURLSessionTask05() {
        let configuration = NSURLSessionConfiguration.backgroundSessionConfigurationWithIdentifier("backgroundSession")
        let session = NSURLSession(configuration: configuration, delegate: self, delegateQueue: NSOperationQueue.mainQueue())
        let url = NSURL(string: "https://google.com")!
        self.exceptation = self.expectationWithDescription("task")
        let downloadTask = session.downloadTaskWithURL(url)
        
        var summary = "Suspended, request={https://google.com}"
        self.compareObject(downloadTask, type: "NSURLSessionDownloadTask", summary: summary)
        downloadTask.resume()
        summary = "Running, request={https://google.com}"
        self.compareObject(downloadTask, type: "NSURLSessionDownloadTask", summary: summary)
        
        self.waitForExpectationsWithTimeout(2, handler: nil)
    }
    
    func URLSession(session: NSURLSession, downloadTask: NSURLSessionDownloadTask, didFinishDownloadingToURL location: NSURL) {
        let summary = "Running, received=\(downloadTask.countOfBytesReceived), request={https://google.com}, response={\(downloadTask.response!.URL!.absoluteString!)}"
        self.compareObject(downloadTask, type: "NSURLSessionDownloadTask", summary: summary)
        
        self.exceptation?.fulfill()
    }
}
