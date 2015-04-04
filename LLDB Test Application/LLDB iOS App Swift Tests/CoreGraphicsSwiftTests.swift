//
//  CoreGraphicsSwiftTests.swift
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

import UIKit
import XCTest

class CoreGraphicsSwiftTests: SharedSwiftTestCase {
    
    // MAKR: - Setup
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testTrue() {
        XCTAssertTrue(true)
    }

    // MARK: - CGPoint
//    func testCGPoint() {
//        let point = CGPoint(x: 1, y: 2)
//        self.compareVariable(point, type: "CGPoint", summary: "(x = 1, y = 2)")
//    }

    // MARK: - CGSize
//    func testCGSize() {
//        let size = CGSize(width: 3, height: 4)
//        self.compareVariable(size, type: "CGSize", summary: "(width = 3, height = 4)")
//    }
    
    // MARK: - CGRect
//    func testCGRect() {
//        let rect = CGRect(x: 6, y: 7, width: 8, height: 9)
//        self.compareVariable(rect, type: "CGRect", summary: "(origin = (x = 6, y = 7), size = (width = 8, height = 9))")
//    }
    
    // MARK: - CGVector
//    func testCGVector() {
//        let vector = CGVector(dx: 3, dy: 5)
//        self.compareVariable(vector, type: "CGVector", summary: "(dx = 3, dy = 5)")
//    }
    
    // MARK: - CGAffineTransform
//    func testCGAffineTransform() {
//        let transofrm = CGAffineTransform(a: 2, b: 3, c: 4, d: 5, tx: 6, ty: 7)
//        self.compareVariable(transofrm, type: "CGAffineTransform", summary: "([2, 3], [4, 5], [6, 7])")
//    }
}
