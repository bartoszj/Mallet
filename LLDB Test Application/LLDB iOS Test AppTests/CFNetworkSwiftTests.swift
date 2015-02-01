//
//  CFNetworkSwiftTests.swift
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

import UIKit
import XCTest

class CFNetworkSwiftTests: SharedSwiftTestCase {

    // MARK: - Setup
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
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
        let request = mutableRequest.copy() as NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "https://google.com")
    }

    func testNSURLRequest3() {
        // HTTP Method.
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        mutableRequest.HTTPMethod = "POST"
        let request = mutableRequest.copy() as NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "POST, https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "POST, https://google.com")
    }
    
    func testNSURLRequest4() {
        // HTTP Body.
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        mutableRequest.HTTPBody = "httpBodyData".dataUsingEncoding(NSUTF8StringEncoding)
        let request = mutableRequest.copy() as NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "GET, https://google.com, body=12 bytes")
        self.compareObject(request, type: "NSURLRequest", summary: "GET, https://google.com, body=12 bytes")
    }
    
    func testNSURLRequest6() {
        let url = NSURL(string: "https://google.com")!
        let mutableRequest = NSMutableURLRequest(URL: url)
        var request = mutableRequest.copy() as NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "https://google.com")
        
        // HTTP headers.
        mutableRequest.setValue("headerValue", forHTTPHeaderField: "headerName")
        mutableRequest.setValue("headerValue2", forHTTPHeaderField: "headerName2")
        request = mutableRequest.copy() as NSURLRequest
        self.compareObject(mutableRequest, type: "NSMutableURLRequest", summary: "GET, https://google.com")
        self.compareObject(request, type: "NSURLRequest", summary: "GET, https://google.com")
    }
}
