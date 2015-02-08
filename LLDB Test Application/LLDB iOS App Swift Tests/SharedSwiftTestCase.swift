//
//  SharedSwiftTestCase.swift
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

import UIKit
import XCTest

class SharedSwiftTestCase: XCTestCase {

    func doNothing() {
        
    }
    
    func compareVariable(variable: Any, type: String, summary: String) -> NSNumber? {
        var equal: NSNumber? = nil
        // Set breakpoint here:
        // compare_summary variable type summary equal 1
        
        self.doNothing()
        
        XCTAssertNotNil(equal, "Python script doesn't work.")
        XCTAssertTrue(equal!.boolValue, "Wrong summary.")
        
        return equal
    }
    
    func compareObject(object: AnyObject, type: String, summary: String) -> NSNumber? {
        var equal: NSNumber? = nil
        // Set breakpoint here:
        // compare_summary object type summary equal 1
        
        self.doNothing()
        
        XCTAssertNotNil(equal, "Python script doesn't work.")
        XCTAssertTrue(equal!.boolValue, "Wrong summary.")
        
        return equal
    }
}
