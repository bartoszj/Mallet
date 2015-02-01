//
//  QuartzCoreSwiftTests.swift
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

import UIKit
import XCTest

class QuartzCoreSwiftTests: SharedSwiftTestCase {

    // MARK: - Setup
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }

    // MARK: - CALayer
    func testCALayer1() {
        let layer = CALayer()
        layer.position = CGPoint(x: 1, y: 2)
        layer.bounds = CGRect(x: 1, y: 2, width: 160, height: 161)
        
        self.compareObject(layer, type: "CALayer", summary: "position=(1, 2), bounds=(1 2; 160 161)")
    }
}
